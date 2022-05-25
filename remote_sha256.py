#!/usr/bin/env python3
"""
Connect to a remove server and calculate the SHA256 checksums for a given directory,
saving the results locally.
"""
import argparse
import traceback
import sys
import random
import time
from pathlib import Path
from _socket import gaierror
import paramiko
from paramiko import SSHException, SSHClient, AutoAddPolicy

# pylint: disable=line-too-long
# pylint: disable=unused-variable
def remote_sha256(
        *,
        server: str,
        retries: int,
        remotepath: str,
        report: str
):
    """
    Connect to a remote server and calculate the SHA256 checksums. The script uses public authentication and expects
    an RSA private/public key to be ready on both local and remote servers.
    :param server: Remote server
    :param retries: Number of retries
    :param remotepath: Path where the files that need an SHA256 checksum calculated reside
    :param report: Local path for the generated report
    :return: None
    """
    with SSHClient() as client:
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())
        key = paramiko.rsakey.RSAKey.from_private_key_file(str(Path.home().joinpath('.ssh').joinpath('id_rsa')))
        attempt = 1
        while attempt < retries:
            try:
                client.connect(hostname=server, pkey=key, banner_timeout=300, timeout=300)
                remote_cmd = f'/usr/bin/find {remotepath} -type f| /usr/bin/xargs /usr/bin/sha256sum --binary'
                print(f"SSH connected to {server}, getting remote checksums. It will take a while...")
                stdin, stdout, stderr = client.exec_command(remote_cmd)
                with open(report, 'w') as rfh:
                    for line in stdout.readlines():
                        rfh.write(line)
                        print(line.strip(), file=sys.stdout)
                for line in stderr.readlines():
                    print(line.strip(), file=sys.stderr)
                break
            except (SSHException, gaierror):
                wait_time = int(random.uniform(1, 60))
                print(f"ERROR: Could not connect, will try again in {wait_time} seconds ({attempt})", file=sys.stdout)
                print("-" * 60)
                traceback.print_exc(file=sys.stdout)
                print("-" * 60)
                time.sleep(wait_time)
                attempt += 1


def main(params: dict[any, any]) -> dict[any, any]:
    """
    Calculate and collect the SHA256 from files on a remote server
    :param params: Dictionary with required arguments
    :return: Any output for the user, as described here: https://docs.airplane.dev/tasks/output
    """
    server = params['server']
    retries = params['retries']
    remotepath = params['remotepath']
    report = params['report']
    remote_sha256(
        server=server,
        remotepath=remotepath,
        report=report,
        retries=retries
    )
    return {"results": f"SHA256 collected and calculated from  {server}:{remotepath} was written to {report}"}


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        description='Calculate the checksum of remote files to make sure they are not tampered')
    PARSER.add_argument('--retries', action='store', default=10, help='SSH retry override')
    PARSER.add_argument('--server', action='store', required=True, help='Name of the remote server with the files')
    PARSER.add_argument('--remotepath', action='store', required=True,
                        help='Remote path with files that need will get their sha256 calculated')
    PARSER.add_argument('report', action='store', help='Report destination')
    ARGS = PARSER.parse_args()
    main({
        'server': ARGS.server,
        'retries': ARGS.retries,
        'remotepath': ARGS.remotepath,
        'report': ARGS.report
    })
