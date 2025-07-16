# -*- coding: utf-8 -*-
"""
Created on Thu May 27 10:16:24 2021
Question:
    1. How to simulate machine operation?
    
Steps: 
    1.  add image by using 'template' function of dashboard
    https://discourse.nodered.org/t/how-to-display-an-image-on-node-red-dashboard-using-template-node/24734/5  
    
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
topic_s = 'mislab/id/xy'    # topic for sending mqtt message
topic_r = 'mislab/id/ctl'   # topic for receiving mqtt messgae

timer_enable = True      # enable/disable the timer
smpPeriod = 1            #sample period in sec
eqlist = ['EQ1', 'EQ2']
eq = {'EQ1':{'state':'start', 'job':30}, 
      'EQ2':{'state':'start', 'job':65}}

# In[1]: Sending messages to Internet      
class Sender(object):
    
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
        msg={'Equipment':{}}
        now = datetime.datetime.now()
        msg['Time'] = now.strftime("%d/%m/%Y %H:%M:%S")
        for t in eqlist:
            msg['Equipment'][t] = eq[t]
        jmsg = json.dumps(msg, ensure_ascii = False)    # transform message in Json format
        return [jmsg]   
    
# In[2]: receiving message from Internet
class Receiver(object):
    
    def __init__(self, period=3):
        self.pd = period                                 # set the default time period
    
    def run(self):
        subscribe.callback(self.unpackmsg, topic_r, hostname=host)
        
    def unpackmsg(self, client, userdata, message):
        global eq 
        r_msg = ast.literal_eval(message.payload.decode("UTF-8"))
        eq['EQ1']['state'] = r_msg['EQ1']['state']
        eq['EQ1']['job'] = int(r_msg['EQ1']['job'])
        print(eq)
    
# In[3]: Machine Simulator
class Simulator(object):
    
    def __init__(self, period=1):
        self.pd = period                                 # set the default time period
    
    def run(self):
        global timer_enable, eq 
        while (timer_enable):
            for t in eqlist:
                if eq[t]['state'] == 'start':
                    if eq[t]['job'] > 0:
                        eq[t]['job'] = eq[t]['job'] -1
                        eq[t]['Data'] =  round(random(),3)
                    else:
                        eq[t]['state'] = 'stop'
                        eq[t]['Data'] = 0
                            
            time.sleep(self.pd)    
           
# In[2]: Start the threads
if __name__ == '__main__':

    st = Sender(1)                                   # initialize an object 
    send_msg = threading.Thread(target = st.run,  args=())   # set the object to be a thread
    send_msg.start()         
    
    rt = Receiver(1)                                 # initialize an object 
    receive_msg = threading.Thread(target = rt.run,  args=())# set the object to be a thread
    receive_msg.start()  

    sm = Simulator()                                # initialize an object 
    simulator = threading.Thread(target = sm.run,  args=())  # set the object to be a thread
    simulator.start()  
    
    input('Press Any Key to Stop the Timer!')
    timer_enable = False