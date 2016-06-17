# -*- coding: utf-8 -*-

"""
wechat
~~~~~~~~~~~~
alertor for wechat

@author: zhaochf
"""
import ConfigParser
import json
import logging
import os.path
import sys
import requests

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='/tmp/alertor.log',
                filemode='w')


__URL_TEMPLATE_GET_TOKEN = "%s?corpid=%s&corpsecret=%s"
__URL_TEMPLATE_SEND_MESSAGE = "%s?access_token=%s"
    
class wechat(object):
    
    def __init__(self, user, message):
        logging.info('Send to user is: %s' % (user))
        logging.info('Send message is: %s' % (message))
       
        conf = '/conf/alertor.conf'
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
        logging.info('Post messages is: %s' % (self.__data))
        result = requests.post(self.__URL_TEMPLATE_SEND_MESSAGE % (self.__send_message_uri, self.__get_token()), data=self.__data)
        result = json.loads(result.text)
        result = result['errcode']
        logging.info('Post result is: %s' % (result))
        return result

       
def main(argv):
    sys.exit(wechat(argv[1], argv[2]).alert())

if __name__ == '__main__':
    main(sys.argv)