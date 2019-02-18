#!/usr/bin/perl
#############################################################
# Plugin to check login by ssh on GNU/Linux operating systems
#
# Requires Net::OpenSSH
# You can install it from EPEL for RHEL 7 or
# with libnet-openssh-perl on Debian based systems
# Net:OpenSSH requires IO::Tty
# You can install it from optional packages for RHEL 7 or
# with libio-pty-perl on Debian based systems
# Esteban Monge: estebanmonge@riseup.net
# https://github.com/EstebanMonge/nagios-plugins
############################################################
use strict;
use warnings;
use Net::OpenSSH;

my $num_args = $#ARGV + 1;
if ($num_args != 3) {
    print "Usage: check_login.pl username password host\n";
    exit 3;
}

my $username=$ARGV[0];
my $password=$ARGV[1];
my $host=$ARGV[2];

my $ssh = Net::OpenSSH->new("$username:$password\@$host",timeout=>5);
if ($ssh->error) {
  print $ssh->error."\n";
  exit 2;
}
else {
        print "Login sucessfull\n";
        exit 0;
}
