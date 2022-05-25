#!/bin/bash
:<<DOC
You can call the script like this (example below):

[myuser@myserver ~]$ ssh-keygen -t rsa -m PEM
Generating public/private rsa key pair.
Enter file in which to save the key (/home/myuser/.ssh/id_rsa): 
Created directory '/home/myuser/.ssh'.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/myuser/.ssh/id_rsa.
Your public key has been saved in /home/myuser/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:3LPC6w1VPwi9ZrOvKpUjKWIEsaMOOQg9ivJPdgPVqa4 myuser@myserver
The key's randomart image is:
+---[RSA 3072]----+
|  ..             |
| ...   . . .     |
|. =.  . o . o    |
|++ o.. o . o +   |
|X  .. . S.+.* o  |
|+o  oo..o.+= o . |
| ...o.+.+o...    |
|   + o ..=   .   |
|    E  .o.o....  |
+----[SHA256]-----+
DOC
ssh-keygen -t rsa -m PEM
