import os,time

datassid = {
  'ssid':'',
  'password':''
}
with open('datassid.json','w') as file:
  json.dump(datassid,file)

datakey = {
  'topic':'',
  'broker':'',
  'publish':''
}
with open('datakey.json','w') as file:
  json.dump(datakey,file)
  
time.sleep(5)
print('setup to default')


