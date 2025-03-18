import paho.mqtt.client as mqtt
import random
import time
from datetime import date, datetime
import json

#------------------------Publisher:Monitor to APP---------------------------
client1=mqtt.Client()
client1.connect("broker.hivemq.com", 1883)

#--Publisher
while True:
  #Temperature sensor
  # Temperature=random.randint(5,30)
  status = input("Does the door sensor determine that it is in the open state? False:OFF True:ON")
  DoorMesaage="A person is detected to have left"
  day=date.today()    #date function call
  clock=datetime.now()  #time function calls
  time_time=datetime.time(clock)    #exact time step
  data=[DoorMesaage,status,str(day),str(time_time)]    #store all data into
  data_encoded=json.dumps(data)    #encode array 'data' into json data format
  client1.publish("smart_home/door_sensor/data", data_encoded)  #publish data

  #pirint message with data, time and date to check if it is published
  print("Door just published: " + str(DoorMesaage) + "; status-" +str(status), \
        " to topic: 'smart_home/door_sensor/data' \n")
  time.sleep(3) #publish new entry between 3 and 10 seconds
  if status=="False":
    break

# -------------------Subscriber:APP to Monitor-------------------------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
      print("Subscriber connected successfully to Broker with result code:", rc)
      client.subscribe("smart_home/subscriber/command")
    else:
      print("Subscriberconnection failed with result code:", rc)


# def on_message(client, userdata, msg):
#    global message_count
#    try:
#       if message_count>=stop_threshold:
#          client.disconnect()
#       print("Subscriber received message on topic:", msg.topic)
#       data = json.loads(msg.payload.decode("utf-8"))
#       message_count+=1
#       print(data)
#       print()
#    except json.JSONDecodeError:
#       print("Subscriber cannot decode message on topic:", msg.topic)


def on_message(client, userdata, msg):
  global message_count
  try:
    if message_count >= stop_threshold:
      client.disconnect()
    print("Subscriber received message on topic:", msg.topic)
    data = json.loads(msg.payload.decode("utf-8"))
    message_count += 1
    print(data)
    print()
    if data[3]=='exit':
      client.disconnect()
  except json.JSONDecodeError:
    print("Subscriber cannot decode message on topic:", msg.topic)


# 定义计数器和停止阈值
message_count = 0
stop_threshold = 4

client1 = mqtt.Client()
client1.on_connect = on_connect
client1.on_message = on_message
print("After showing five message, it will disconnect")

# Optional authentication
client1.username_pw_set("AA", "qwerty")

# Connect to the broker and start listening
client1.connect("broker.hivemq.com", 1883)

client1.loop_forever()




