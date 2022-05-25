#!/usr/bin/env python3
import argparse
import sys
import traceback

from tabulate import tabulate


def write_report(
        *,
        original_report: str,
        destination_report: str
) -> None:
    with open(original_report, 'rt') as sha256:
        checksum_report = [
            ['SHA256:', 'File:']
        ]
        with open(destination_report, 'wt') as report:
            for line in sha256:
                checksum, orig_file = line.split()
                checksum_report.append([checksum, orig_file.replace("*", "")])
            report.writelines(tabulate(checksum_report, headers="firstrow", tablefmt="simple"))


def main(params: dict[any, any]) -> dict[any, any]:
    """
    Entry point for the Airplane task
    :param params: Dictionary with required arguments
    :return: Any output for the user, as described here: https://docs.airplane.dev/tasks/output
    """
    original = params['original_report']
    destination = params['destination_report']
    write_report(original_report=original, destination_report=params['destination_report'])
    return {"results": f"SHA256 table report from {original} was written to {destination}"}


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Create a nice table report from calculated SHA256 checksums')
    PARSER.add_argument('--sha256report', action='store', default=10, help='Original SHA256 report')
    PARSER.add_argument('report', action='store', help='Table report')
    ARGS = PARSER.parse_args()
    try:
        main({
            'original_report': ARGS.sha256report,
            'destination_report': ARGS.report
        })
    except ValueError:
        print("-" * 60)
        traceback.print_exc(file=sys.stdout)
        print("-" * 60)
