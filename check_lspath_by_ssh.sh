#!/bin/bash
##########################################################
# Plugin to check NTP and Chrony via SSH to avoid use of agents
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

output=$(ssh $host '/usr/sbin/lspath|grep -v "Enabled"')

if [[ -z "$output" ]]
then
        echo "OK - All paths enabled"
        exit 0
else
        echo "CRITICAL - Path with problems $output"
        exit 2
fi
