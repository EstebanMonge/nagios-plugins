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

performance=$(ssh $host 'uptime' 2> /dev/null )
output=$(echo $performance | awk '{print $3,$4}')

case $performance in
        *min*)
                echo $performance | awk '{print $3}'
                ;;
        *day*)
                time_today=$(echo $performance | awk '{print $1}')
                total_seconds=$(($(date -u -d "$time_today" +"%s")-$(date -u -d "12:00AM" +"%s")))
                minutes_today=$((total_seconds/60))
                total_minutes=$(echo $performance | awk '{print $3*24*60}')
                performance=$((total_minutes+minutes_today))
                ;;
        *)
                time_uptime=$(echo $performance | awk '{print $3}')
                performance=$(echo $time_uptime | awk -F: '{print $1*60+$2}')
                ;;
esac

case $output in
        0-1) echo "CRITICAL - Uptime: ${output//,} | uptime_minutes=$performance"
           exit 2
           ;;
        *min*) echo "CRITICAL - Uptime: ${output//,} | uptime_minutes=$performance"
           exit 2
           ;;
        "") echo "CRITICAL - I can't get uptime. Agüevado"
            exit 2
            ;;
        *) echo "OK - Uptime: ${output//,} | uptime_minutes=$performance"
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
