#!/bin/bash
##########################################################
# Plugin to check NTP and Chrony via SSH to avoid use of agents
# Esteban Monge: estebanmonge@riseup.net
############################################################


help(){
PROGNAME=`basename $0`
cat << END
Usage :
        $PROGNAME [Hostname or IP] [NTP Client]
        OPTION          DESCRIPTION
        ----------------------------------
        NTP Client      It can be 'chrony' or 'ntp'
        ----------------------------------
END
}
host=$1
ntp_client=$2

if [[ $host == "" ]]
then
        help
        exit 3
fi

case $ntp_client in
        chrony)
                output=$(ssh $host 'chronyc tracking|grep -e "Leap status"')
                ;;

        ntp)
                output=$(ssh $host 'ntpstat |grep synchronised')
                ;;
        *) help
                exit 3
                ;;
esac

if [[ $output == *"Normal"* || $output == *"synchronised to NTP server"* ]]
then
        echo "OK - $output"
        exit 0
else
        echo "CRITICAL - $output"
        exit 2
fi

