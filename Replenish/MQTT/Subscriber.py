# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 21:51:19 2017
https://internetofthingsagenda.techtarget.com/definition/MQTT-MQ-Telemetry-Transport

@author: ASUS
"""
#%% Subscriber.py
import paho.mqtt.subscribe as subscribe

# host = "broker.emqx.io"
host = 'localhost'  #'127.0.0.1'
portNo = 1883

def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))

# In[1]
# Test 1: start first to subscribe mqtt message by "mislab/mqtt/simple" 
    
msg = subscribe.simple("mislab/id/xy", hostname=host)
print("I got mqtt: %s with %s" % (msg.topic, msg.payload))

# In[2]
# Test 2: start first to subscribe mqtt message by "mislab/mqtt/callback" without stop

subscribe.callback(on_message_print, "mislab/mqtt/simple", hostname=host)

# In[3]
# Test 3: start first to subscribe mqtt message by "mislab/mqtt/multiple" without stop

subscribe.callback(on_message_print, "mislab/id/xy", hostname=host)

# In[4]
# Test 4: use another MQTT Server

host = "m14.cloudmqtt.com" 
portNo = 	17640 
authpass = {'username':"vfhmwuwd", 'password':"9Na3SdDn7KvW"}
subscribe.callback(on_message_print, "mislab/mqtt/cloudmqtt", hostname=host, port = portNo, auth = authpass)

# In[5] : http://www.steves-internet-guide.com/mosquitto-tls/
host = "localhost"
portNo = 	1883
    
subscribe.callback(on_message_print, "mislab/id/xxx-1", hostname=host)
