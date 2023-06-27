from umqtt.simple import MQTTClient
import network
import json
import time

net = network.WLAN(network.STA_IF)
net.active(True)

while True:
	try:
		net.connect('Office_CWG', 'Unais2020')
	except OSError as e:
		print(e)
	time.sleep(1)
	if net.isconnected():
		print('Connected') 
		break
client = mqtt('','broker.hivemq.com')
client.connect()
print('connect..')

def sub_cb(topic,msg):
  pesan = json.loads(str(msg.decode()))
  alertpowerfactor = int(pesan['alertpf'])
  alerthourenergy = int(pesan['alerthe'])
  alertambiencetemperature = int(pesan['alertat'])
  alertjointemperature = int(pesan['alertjt'])
  if alertpowerfactor == 1 :
    print('power factor dalam keadaan tidak normal')
  if alerthourenergy == 1 :
    print ('hour energy melebihi batas normal')
  if alertambiencetemperature == 1 :
    print ('ambiance temperature melebihi batas normal')
  if alertjointemperature == 1 :
    print ('join temperature melebihi batas normal')
client.set_callback(sub_cb)

client.subscribe('active2')
while True:
  client.check_msg()
