#!/usr/bin/expect
spawn telnet localhost 7505
set timeout 10
expect "OpenVPN Management Interface"
send "status 3\r"
expect "END"
send "exit\r"
