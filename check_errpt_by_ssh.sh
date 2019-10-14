#!/bin/bash
##########################################################
# Plugin to check AIX errpt via SSH to avoid use of agents
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

output=$(ssh $host "errpt | grep \$(date '+%m%d%H')")

if [[ -z "$output" ]]
then
        echo "OK - I not found entries on errpt on last hour"
        exit 0
else
        echo "CRITICAL - I found entries on errpt on last hour: $output"
        exit 2
fi
