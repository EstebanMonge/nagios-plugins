#!/bin/bash
##########################################################
# Plugin to check today messages of auditd
# via SSH to avoid use of agents
# Esteban Monge: estebanmonge@riseup.net
# https://github.com/EstebanMonge/nagios-plugins
############################################################

help(){
PROGNAME=$(basename $0)
cat << END
Usage :
        $PROGNAME [Hostname or IP] [Message type]
END
}
host=$1
message_type=$2

if [[ $host == "" || $message_type == "" ]]
then
        help
        exit 3
fi

output=$(ssh $host "/bin/sudo /usr/sbin/ausearch --input-logs -ts today -m $message_type --raw| /usr/sbin/aureport -f --summary | grep '^[0-9]'" 2> /dev/null )

if [[ -z $output ]]
then
        echo "OK - No $message_type logs found"
        exit 0
else
        echo -e "CRITICAL - I found $message_type logs:\n$output"
        exit 2
fi
