import network,json,math,time
from wmanag import WifiManager
from mqtt import MQTTClient as mqtt

wlan = network.WLAN(network.STA_IF)
#wlan.active(True)

datassid_default = {
  'ssid':'esp32',
  'password':'defaultEsp32'
}
with open('datassid_default.json','w') as file:
  json.dump(datassid_default,file)

datakey_default = {
  'topic':'active1',
  'broker':'broker.hivemq.com',
  'publish':'controller'
}
with open('datakey_default.json','w') as file:
  json.dump(datakey_default,file)

  
  
with open('datassid_default.json','r') as file:
  loadssid_default = json.load(file)
with open('datakey_default.json','r') as file:
  loadkey_default = json.load(file)
  
with open('datassid.json','r') as file:
  loadssid = json.load(file)
with open('datakey.json','r') as file:
  loadkey = json.load(file)
  
if loadssid['ssid']=='' and loadssid['password']=='':
  wm = WifiManager(ssid=loadssid_default['ssid'],password=loadssid_default['password'])
else:
  wm = WifiManager(ssid=loadssid['ssid'],password=loadssid['password'])
  

#wm.web_server()
wm.connect()

while True:
  if wm.is_connected():
    exec(open('active.py').read(),globals())
    #print('connect')
  else:
    print('wifi not connected')
    break
#exec(open('active.py').read(),globals())
