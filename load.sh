#!/bin/bash
##########################################################
#Plugin to check load average of GNU/Linux operating systems

#The default Nagios Plugin allows you to put warning and
#critical thresholds manually but if you have passive checks
#or a lot of servers this can be a nightmare. This plugin
#checks the amount of cpus reported in cpuinfo and use it
#as threshold. Warning for load equal to cpus reported and
#critical for greater than it. The plugin takes loadavg 15
#minutes metric only and compare it with thresholds.
# Esteban Monge estebanmonge@riseup.net
# https://github.com/EstebanMonge/nagios-plugins
##########################################################


#Define variables

label=load
cpu1=$(cat /proc/loadavg | awk '{print $1}')
cpu5=$(cat /proc/loadavg | awk '{print $2}')
cpu15=$(cat /proc/loadavg | awk '{print $3}')
num_cpu=$(grep 'model name' /proc/cpuinfo | wc -l)


if [[ $cpu15 > $num_cpu ]]
then
	echo "Critical - load average $cpu1, $cpu5, $cpu15|load1=$cpu1;0;0;0; load5=$cpu5;0;0;0; load15=$cpu15;$num_cpu;$(($num_cpu+1));0;"
	exit 2 
fi

if [[ $cpu15 == $num_cpu ]]
then
	echo "Warning - load average $cpu1, $cpu5, $cpu15|load1=$cpu1;0;0;0; load5=$cpu5;0;0;0; load15=$cpu15;$num_cpu;$(($num_cpu+1));0;"
	exit 1
fi

if [[ $cpu15 < $num_cpu ]]
then
	echo "Pura vida - load average $cpu1, $cpu5, $cpu15|load1=$cpu1;0;0;0; load5=$cpu5;0;0;0; load15=$cpu15;$num_cpu;$(($num_cpu+1));0;"
	exit 0 
fi
