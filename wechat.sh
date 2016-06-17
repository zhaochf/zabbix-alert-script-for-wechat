#!/bin/bash
#
# Script for send alert message to wechat
# @author: zhaochf

ALERTOR_HOME=/usr/local/zabbix/share/zabbix/alertscripts/alertor

show_usage()
{
    echo -e "`printf %-4s "Usage: $0"` -u [some body] -m [some alert message]"
    echo -e "`printf %-4s ` Send alter message to user."
    echo -e "`printf %-4s ` Mandatory arguments to long options are mandatory for short options too."
    echo -e "`printf %-4s ` [-h|--help]"
    echo -e "`printf %-4s ` [-v|--version]"
    echo -e "`printf %-4s ` [-c|--user ... ]"
    echo -e "`printf %-4s ` [-t|--message ... ]"
}


show_version()
{
    echo "wechat alertor version: 1.0"
}

# Check has parameters
if [ ! -n "$1" ];then
    show_usage
    exit 0
fi


# Check system has been installed python
command -v python >/dev/null 2>&1 || { echo >&2 "The python it's not installed, Please install python first and then execute this shell."; exit 1; }
type python >/dev/null 2>&1 || { echo >&2 "The python it's not installed, Please install python first and then execute this shell."; exit 1; }
hash python 2>/dev/null || { echo >&2 "The python it's not installed, Please install python first and then execute this shell."; exit 1; }


TEMP=`getopt -o hvu:m: --long help,version,user:,message: -- "$@" 2>/dev/null`
[ $? != 0 ] && echo -e "\033[31mERROR: unknown argument! \033[0m\n" &&  show_usage && exit 1
eval set -- "$TEMP"


while :
do
        [ -z "$1" ] && break
        case "$1" in
                -h|--help)
                        show_usage; exit 0
                        ;;
                -v|--version)
                         show_version; exit 0
                        ;;
                -u|--user)
                        user=$2; shift 2
                        ;;
                -m|--message)
                        message=$2; shift 2
                        ;;
                                --)
                        shift
                        ;;
                *)
                        echo -e "\033[31mERROR: unknown argument!\033[0m\n" && show_usage && exit 1
                        ;;
        esac
done

python $ALERTOR_HOME/wechat.py "$user" "$message"