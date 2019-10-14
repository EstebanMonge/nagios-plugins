help(){
PROGNAME=$(basename $0)
cat << END
Usage :
        $PROGNAME [Hostname or IP] [password age]
        OPTION          DESCRIPTION
        ----------------------------------
        password age      It must be integer
        ----------------------------------
END
}
host=$1
password_age=$2

if [[ $host == "" || $password_age == "" ]]
then
        help
        exit 3
fi

result=$(ssh $host 'for i in $(cat /etc/passwd | awk -F : "{print \$1}"); do expiry_date=$(sudo lchage -l $i | grep "Password Expires"| grep -v Never|cut -d: -f2) && password_expiry_date=$(date -d "$expiry_date" "+%s") && current_date=$(date "+%s") && diff=$(($password_expiry_date-$current_date)) && let DAYS=$(($diff/(60*60*24))) && if [[ $DAYS -le '$password_age' ]]; then echo "$i password will expire in $DAYS days ";fi; done')
if [[ $result ]]
then
        echo "CRITICAL - $result"
        exit 2
else
        echo "OK - No password will expire soon"
        exit 0
fi
