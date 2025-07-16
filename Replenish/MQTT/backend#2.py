'''
Question:
    1. How to publish a messsage in specific structure periodly?
    2. How to extract the specific message from the Web interface?
    
Goal: 
    1. design a compilicated data structure 
    eq = {'EQ1':{'state':'Ready'}, 
          'EQ2':{'state':'Busy'}}
    
    2. new and interactive functions in a class
    3. retrive data from a JSON object
    
Procedure:
    1. run this py code
    2. start node-red server and link http:127.0.0.1:1880
   
Exercise:
    1. modify the data structure of this equipment {'temperature':[27, 28, 22]}
    2. try to show the updated data structure
@author: Horace
'''
import paho.mqtt.publish as publish
import json
from random import random

import time
import threading
import datetime

host = "broker.emqx.io"  # mqtt broker 
portNo = 1883            # mqtt port
topic = 'mislab/id/xy'   # topic for mqtt message

timer_enable = True      # enable/disable the timer
smpPeriod = 3            #sample period in sec
eq = {'EQ1':{'state':'Ready'}, 
      'EQ2':{'state':'Busy'}}

# In[1]: Enable a stable time to triger data collection
#--------------------------------------------------------------------------------------------            
class T0(object):
    
    def __init__(self, period=3):
        self.pd = period                                 # set the default time period
    
    def run(self):
        global timer_enable, eq 
        while (timer_enable):              
            [message] = self.packmsg(eq)
           # print(message)
            publish.single(topic, message, hostname = host)  # publish the message 
            time.sleep(self.pd)                           # wait a time period
    
    def packmsg(self, eq):
        now = datetime.datetime.now()
        msg = {'Time': now.strftime("%d/%m/%Y %H:%M:%S"), 
               'Equipment':{
                   'EQ1': {'state': eq['EQ1']['state'],'Data': round(random(),3)},
                   'EQ2': {'state': eq['EQ2']['state'],'Data': round(random(),3)}
                   }
               }  # format a messgae 
        jmsg = json.dumps(msg, ensure_ascii=False)    # transform message in Json format
        return [jmsg]              
         
# In[2]: Start the timer 
if __name__ == '__main__':

    t0 = T0(smpPeriod)                                    # initialize an object 
    mt = threading.Thread(target = t0.run,  args=())      # set the object to be a thread
    mt.start()     
    timer_enable = True  
    eq['EQ1']['state']='Run'                                       # start the triger timer
    eq['EQ2']['state']='Down'
    input('Press Any Key to Stop the Timer!')
    timer_enable = False
