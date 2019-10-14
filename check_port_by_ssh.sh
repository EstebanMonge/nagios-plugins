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
        $PROGNAME [Hostname or IP] [OS] [Remote host] [Remote tcp port]
        OPTION          DESCRIPTION
        --------------------------------------------------
        OS             It can be 'linux' or 'aix'
        Remote host    Remote host to check port
        Remote port    Remote port to check on remote host
        --------------------------------------------------
END
}
host=$1
os=$2
remote_host=$3
remote_port=$4

if [[ $host == "" || $remote_host == "" || $remote_port == "" ]]
then
        help
        exit 3
fi

case $os in
        linux)
                output=$(ssh $host "timeout 2 bash -c \"cat < /dev/null > /dev/tcp/$remote_host/$remote_port\" && echo $?")
                ;;

        aix)
                output=$(ssh $host 'sudo ntpq -pn | grep -F "*" | awk "{print \$1,\"offset\",\$9}"|cut -d "*" -f 2')
                ;;
        *) help
                exit 3
                ;;
esac

if [[ ! -z "$output" ]]
then
        echo "OK - I could open port $remote_port on host $remote_host"
        exit 0
else
        echo "CRITICAL - I could not open port $remote_port on host $remote_host"
        exit 2
fi
