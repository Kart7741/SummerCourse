# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 21:56:59 2017
https://internetofthingsagenda.techtarget.com/definition/MQTT-MQ-Telemetry-Transport

@author: ASUS
"""

#%% Publisher.py
import paho.mqtt.publish as publish
import json

# host = "broker.emqx.io"
host = 'localhost'  #'127.0.0.1'
portNo = 1883

msg = {"subject":"Math","score":100}  # example message
jmsg = json.dumps(msg, ensure_ascii=False)  # convert to JSON string

# In[1]
# Test 1: start later to publish mqtt message by "mislab/mqtt/simple" 

publish.single("mislab/id/xy", jmsg, hostname= host)

# In[2]
# Test 2: start later to publish mqtt message by "mislab/mqtt/callback" 

publish.single("mislab/id/xxx-2", jmsg, hostname = host, qos=1)
'''
      QOS 0: The client will deliver the message once, with no confirmation.
      QOS 1: The client will deliver the message at least once, with confirmation required.
      QOS 2: The client will deliver the message exactly once by using a four step handshake.
'''

# In[3]
# Test 3: start later to publish mqtt message by "mislab/mqtt/multiple" 

msgs = [{'topic':"mislab/mqtt/multiple",'payload': "multiple 1"},
        ("mislab/mqtt/multiple", 'multiple 2', 0, False)]
publish.multiple(msgs, hostname = host)
'''
the form must be: ("<topic>", "<payload>", qos, retain)
      qos: QOS 0, 1, 2
      retain: 
         http://www.steves-internet-guide.com/mqtt-retained-messages-example/
'''
# In[4]
# Test 4: use another MQTT Server
# start later to publish mqtt message by 'mislab/mqtt/callback' 

host = "m14.cloudmqtt.com" 
portNo =  17640 
authpass = {'username':"vfhmwuwd", 'password':"9Na3SdDn7KvW"}

publish.single("mislab/mqtt/cloudmqtt", jmsg, hostname= host, port = portNo, auth = authpass)

# In[5]
'''
Running Mosquitto:
To start the broker, open a command prompt by clicking on Start | All Programs | Accessories | Command Prompt.
In the command prompt, navigate to the Mosquitto root folder, such as C:\Program Files\mosquitto.
Start the Mosquitto service by running the command: "net start mosquitto".
Acknowledge the message: The Mosquitto Broker service was started successfully.
'''
host = "127.0.0.1"
portNo = 	1883
msgs = [{'topic':'mislab/id/xxx-1','payload': "multiple 1"},
        ('mislab/id/xxx', 'multiple xyz', 0, False),
        ('mislab/id/xyz', 'hello')]

jmsg = json.dumps(msgs, ensure_ascii=False)
publish.multiple(msgs, hostname= host)
