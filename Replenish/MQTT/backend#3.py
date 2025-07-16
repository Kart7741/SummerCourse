# -*- coding: utf-8 -*-
"""
Created on Thu May 27 10:16:24 2021
Question:
    1. How to receive a messsage from Web and update the states back?
    
Goal: 
    1. update topics    
    2. add a new thread for receiving message
   
Exercise:
    1. receiving various messages from UI
@author: hao
"""

import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import json
from random import random

import ast
import time
import threading
import datetime

host = "broker.emqx.io"     # mqtt broker 
portNo = 1883               # mqtt port
topic_s = 'mislab/id/xy-1'    # topic for sending mqtt message
topic_r = 'mislab/id/ctlx'   # topic for receiving mqtt messgae

timer_enable = True      # enable/disable the timer
smpPeriod = 1            #sample period in sec
eq = {'EQ1':{'state': 0}, 
      'EQ2':{'state': 0}}

# In[1]: Sending messages to Internet
class T0(object):
    
    def __init__(self, period=3):
        self.pd = period                                 # set the default time period
    
    def run(self):
        global timer_enable, eq 
        while (timer_enable):              
            [message] = self.packmsg(eq)
           # print(message)
            publish.single(topic_s, message, hostname = host)  # publish the message 
            time.sleep(self.pd)                           # wait a time period
    
    def packmsg(self, eq):
        now = datetime.datetime.now()
        msg = {'Time': now.strftime("%d/%m/%Y %H:%M:%S"), 
               'Equipment':{
                   'EQ1': {'state': eq['EQ1']['state'],'Data': round(random(),3)},
                   'EQ2': {'state': eq['EQ2']['state'],'Data': round(random(),3)}
                   }
               }  # format a messgae 
        jmsg = json.dumps(msg, ensure_ascii = False)    # transform message in Json format
        return [jmsg]   
    
# In[2]: receiving message from Internet
           
class T1(object):
    
    def __init__(self, period=3):
        self.pd = period                                 # set the default time period
    
    def run(self):
        subscribe.callback(self.unpackmsg, topic_r, hostname=host)
        
    def unpackmsg(self, client, userdata, message):
        r_msg = ast.literal_eval(message.payload.decode("UTF-8"))
        print(repr(r_msg))
        if r_msg['EQ1'] == 'Start':
            eq['EQ1']['state'] = 1
        else: 
         if r_msg['EQ1'] == 'Stop':
            eq['EQ1']['state'] = 0
           
# In[3]: Start the timer threads
if __name__ == '__main__':

    t0 = T0(smpPeriod)                                      # initialize an object 
    send_msg = threading.Thread(target = t0.run,  args=())  # set the object to be a thread
    send_msg.start()         
    
    t1 = T1(smpPeriod)                                      # initialize an object 
    receive_msg = threading.Thread(target = t1.run,  args=())      # set the object to be a thread
    receive_msg.start()  
    
    input('Press Any Key to Stop the Timer!')
    timer_enable = False