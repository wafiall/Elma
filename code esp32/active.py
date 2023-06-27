
import network 
import json
import time
import uPZEM_004t
import machine

from umqtt.simple import MQTTClient as mqtt

wlan = network.WLAN(network.STA_IF)
  
if wlan.isconnected():
  print('WIFI connected to '+wlan.config('essid'))
  #topicx = globals()['topicx']
    
  with open('datakey.json', 'r') as file:
    xx = json.load(file)
  

  device = xx['broker']
  topic_pub = xx['publish']
  
  client = mqtt('',device,user='median',password='median2022')
  client.connect()
  
  def read_lm35_temperature():
    reading = adc.read()  # Baca nilai ADC
    voltage = reading * 3.3 / 4095  # Konversi nilai ADC ke tegangan
    temperature = voltage * 100  # Konversi tegangan menjadi suhu dalam derajat Celsius
    return temperature
  
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

  client.subscribe(xx['topic'])
  while True:
    pzem = uPZEM_004t.uPZEM(1,pins=[17,16])
    adc = machine.ADC(machine.Pin(34))  
    adc.atten(machine.ADC.ATTN_11DB) 
    temperature = read_lm35_temperature()

    client.check_msg()
    
    sensor = {
      'pub': xx['topic'],
      'current': pzem.read_input_registers(1)[1],
      'volt': pzem.read_input_registers(1)[0],
      'frekuensi': pzem.read_input_registers(1)[4],
      'activePower': pzem.read_input_registers(1)[2],
      'energy': pzem.read_input_registers(1)[3],
      'power factor':pzem.read_input_registers(1)[5],
      'ambienceTemperature': temperature,
      'jointTemperature': '32'
    }
    data = json.dumps(sensor)
    
    client.publish(topic_pub, data)
    time.sleep(5)
    print('success sent a message')

else:
  print('saknsak')

