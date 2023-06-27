import json

data = ''
with open('dataxx.json','w') as file:
  json.dump(data,file)

with open('dataxx.json','r') as file:
  dodo = json.load(file)

if dodo == "":
  print('cxc')
else:
  print('kaso')
