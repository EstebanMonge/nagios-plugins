#!/bin/bash
##########################################################
# Plugin to check uptime via SSH to avoid use of agents
# Works on AIX, Debian and RHEL alike GNU/Linux 
# Esteban Monge: estebanmonge@riseup.net
# https://github.com/EstebanMonge/nagios-plugins
############################################################


help(){
PROGNAME=$(basename $0)
cat << END
Usage :
        $PROGNAME [Hostname or IP]
END
}
host=$1

if [[ $host == "" ]]
then
        help
        exit 3
fi

output=$(ssh $host 'uptime' 2> /dev/null | awk '{print $3,$4}' )

case $output in
	0-1) echo "CRITICAL - Uptime: ${output//,}"
	   exit 2
	   ;;
	*min*) echo "CRITICAL - Uptime: ${output//,}"
	   exit 2
	   ;;
        "") echo "CRITICAL - I can't get uptime. Agüevado"
	    exit 2
	    ;;
	*) echo "OK - Uptime: ${output//,}"
           exit 0
	   ;;
esac
        

if [[ $output != "0" && $output != "1" && $output != "" ]]
then
        echo "OK - Uptime: $output"
        exit 0
else
        echo "CRITICAL - Uptime: $output"
        exit 2
fi
