# -*- coding: utf-8 -*-

"""
wechat
~~~~~~~~~~~~
alertor for wechat

@author: zhaochf
"""
import ConfigParser
import requests
import json
import sys
import getopt

__URL_TEMPLATE_GET_TOKEN = "%s?corpid=%s&corpsecret=%s"
__URL_TEMPLATE_SEND_MESSAGE = "%s?access_token=%s"
    
class wechat(object):
    
    def __init__(self, user, message):
       
        conf = 'conf/alertor.conf'
        config = ConfigParser.ConfigParser()
        config.read(conf)

        self.__URL_TEMPLATE_GET_TOKEN = '%s?corpid=%s&corpsecret=%s'
        self.__URL_TEMPLATE_SEND_MESSAGE = '%s?access_token=%s'
        self.__crop_id = config.get('wechat', 'CropId')
        self.__secret = config.get('wechat', 'Secret')
        self.__get_token_uri = config.get('wechat', 'TokenURI')
        self.__send_message_uri = config.get('wechat', 'MessageURI')
        self.__data = '{\n\
            "touser":"%s",\n\
            "toparty":"1",\n\
            "totag":"@all",\n\
            "msgtype":"text",\n\
            "agentid":"2",\n\
            "text":{\
                "content":"%s"\n\
            },\n\
            "safe":"0",\n}' % (user, message)
    
    def __get_token(self):
        result = requests.get(self.__URL_TEMPLATE_GET_TOKEN % (self.__get_token_uri, self.__crop_id, self.__secret)) 
        result = json.loads(result.text)
        return result['access_token'].encode('utf-8')
    
    def alert(self):
        result = requests.post(self.__URL_TEMPLATE_SEND_MESSAGE % (self.__send_message_uri, self.__get_token()), self.__data)
        result = json.loads(result.text)
        return result['errcode']


def usage():
    print 'Usage:'
    print 'wechat.sh -u user -m message'
    print 'Send message to userid'
    print 'Mandatory arguments to long options are mandatory for short options too.'
    print '-h, --help: print help message.'
    print '-v, --version: print script version'
    print '-u, --user: send message to user'
    print '-m, --message: send for message '
    
def version():
    print 'wechat.py 1.0.0'
    
def OutPut(args):
    print 'Hello, %s'%args
        
def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'hvu:m:', ['help', 'version', 'user=', 'message='])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(1)
 
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-v', '--version'):
            version()
            sys.exit(0)
        elif opt in ('-u', '--user'):
            user = arg
        elif opt in ('-m', '--message'):
            message = arg
        else:
            print '\033[31mERROR: unknown argument! \033[0m\n'
            usage()
            sys.exit(1)

    sys.exit(wechat(user, message).alert())

if __name__ == '__main__':
    main(sys.argv)