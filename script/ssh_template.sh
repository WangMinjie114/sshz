#!/usr/bin/expect
set timeout 30
spawn ssh -l USERNAME -p PORT IPADDR ARGVS
expect "assword:"
send "PASSWORD\r"
interact
