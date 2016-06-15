#!/bin/bash
#
# Script for send alert message to wechat
# @author: zhaochf

# Check system has been installed python
command -v python >/dev/null 2>&1 || { echo >&2 "The python it's not installed, Please install python first and then execute this shell."; exit 1; }
type python >/dev/null 2>&1 || { echo >&2 "The python it's not installed, Please install python first and then execute this shell."; exit 1; }
hash python 2>/dev/null || { echo >&2 "The python it's not installed, Please install python first and then execute this shell."; exit 1; }

TEMP=`getopt -o hvu:m: --long help,version,user:,message: -- "$@" 2>/dev/null`
[ $? != 0 ] && echo -e "\033[31mERROR: unknown argument! \033[0m\n" &&  python ./wechat.py -h && exit 1
eval set -- "$TEMP"

while :
do
        [ -z "$1" ] && break
        case "$1" in
                -h|--help)
                        python ./wechat.py -h; exit 0
                        ;;
                -v|--version)
                         python ./wechat.py -v; exit 0
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
                        echo -e "\033[31mERROR: unknown argument!\033[0m\n" && python ./wechat.py -h && exit 1
                        ;;
        esac
done

python ./wechat.py --user=$user --message=$message
exit $?

