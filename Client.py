import paho.mqtt.client as mqtt
import json
from datetime import date, datetime
import time


#------------------Subscriber:Monitor to APP-------------------------------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Subscriber connected successfully to Broker with result code:", rc)
        client.subscribe("smart_home/door_sensor/data")
    else:
        print("Subscriberconnection failed with result code:", rc)

def on_message(client, userdata, msg):
    global message_count1
    try:
        if message_count1>=stop_threshold:
            client.disconnect()
        print("Subscriber received message on topic:", msg.topic)
        data = json.loads(msg.payload.decode("utf-8"))
        message_count1 += 1
        print(data)
        if data[1]=='False':
            print("door sensor closes")
            client.disconnect()
    except json.JSONDecodeError:
        print("Subscriber cannot decode message on topic:", msg.topic)

# 定义计数器和停止阈值
message_count1 = 0
stop_threshold = 4
client1 = mqtt.Client()
client1.on_connect = on_connect
client1.on_message = on_message

# Optional authentication
client1.username_pw_set("AA", "qwerty")

# Connect to the broker and start listening
client1.connect("broker.hivemq.com", 1883)
print("After showing five message, it will disconnect")

client1.loop_forever()

#------------------------Publisher:APP to Monitor---------------------------
client1=mqtt.Client()
client1.connect("broker.hivemq.com", 1883)
while True:
  #Temperature sensor
  # Temperature=random.randint(5,30)
  nowstep=input("Now step:Whether to exit? continue:0 exit:1")

  if nowstep == "1":
    DoorMesaage="No command"
  else:
    status = input("What instructions do you want to send? close_door:0 open_door:1")
    DoorMesaage = "Close the door" if status == '0' else "Open the door"
  # nextstep=input("Next step:Whether to exit? continue:0 exit:1")
  day = date.today()  # date function call
  clock = datetime.now()  # time function calls
  time_time = datetime.time(clock)  # exact time step
  # data=[DoorMesaage,bool(status),str(day),str(time_time),"continue" if nextstep=='0' else "exit"]    #store all data into
  data = [DoorMesaage, str(day), str(time_time),
          "continue" if nowstep == '0' else "exit"]  # store all data into
  data_encoded = json.dumps(data)  # encode array 'data' into json data format
  client1.publish("smart_home/subscriber/command", data_encoded)  # publish data

  # pirint message with data, time and date to check if it is published
  print("Client published: " + str(DoorMesaage)  +  \
        " to topic: 'smart_home/subscriber/command' \n")
  time.sleep(3)  # publish new entry between 3 and 10 seconds
  if nowstep == "1":
    break


