'''
Question:
    How to publish a simple messsage periodly?
Goal: 
    1. use a timer thread to pubish a message per a timer period
    2. recevive the message from a Web-interfcae by Node-red
    
Procedure:
    1. run this py code
    2. start node-red server and link http:127.0.0.1:1880

Exercise:
    1. check the time delay when using different brokers (from remote to local)
@author: Horace
'''
import paho.mqtt.publish as publish
import json

import time
import threading
import datetime
from random import random

host = "broker.emqx.io"  # mqtt broker 
portNo = 1883            # mqtt port
topic = 'mislab/id/xy'   # topic for mqtt message

timer_enable = True      # enable/disable the timer
smpPeriod = 3            #sample period in sec

# In[1]: Enable a stable time to triger data collection
#--------------------------------------------------------------------------------------------            
class T0(object):
    
    def __init__(self, period=3):
        self.pd = period                                 # set the default time period
    
    def run(self):
        global timer_enable 
        ts = datetime.datetime.now().timestamp() # get the start time
        while (timer_enable):              
            now = datetime.datetime.now()
            tf = now.timestamp()                 # get time current time  
            msg = {'Time': now.strftime("%d/%m/%Y %H:%M:%S"), 'dt': str(round(tf-ts,3)),
                   'Temperature': round(random()*40,1)}   # format a messgae 
            jmsg = json.dumps(msg, ensure_ascii=False)    # transform message in Json format
            publish.single(topic, jmsg, hostname = host)  # publish the message 
            ts=tf
            time.sleep(self.pd)                           # wait a time period
            
# In[2]: Start the timer 
if __name__ == '__main__':

    t0 = T0(smpPeriod)                                    # initialize an object 
    mt = threading.Thread(target = t0.run,  args=())      # set the object to be a thread

    mt.start()                                            # start the triger timer

    input('Press Any Key to Stop the Timer!')
    timer_enable = False
