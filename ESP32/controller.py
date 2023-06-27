from umqtt.simple import MQTTClient
import network
import json
import time
import math

while True:
	try:
		net.connect('Vito', 'persib1933a')
	except OSError as e:
		print(e)
	time.sleep(1)
	if net.isconnected():
		print('Connected') 
		break
    

client = mqtt('','broker.hivemq.com')
client.connect()
print('connect..')

def sub_cb(topic, msg):
    pesan = json.loads(str(msg.decode()))
    for x in pesan['data']:
        current = float(x['current'])
        volt = float(x['volt'])
        frekuensi = float(x['frekuensi'])
        ActivePower = float(x['activePower'])
        energy = float(x['activePower'])
        ambienceTemperature = float(x['ambienceTemperature'])
        jointTemperature = float(x['jointTemperature'])
        topic = str(x['topic'])
    
    if current > 0 and volt > 0 and frekuensi >0: 
            # rumus
            ApparentPower = volt*current # daya semu(VA)  
            powerf = ActivePower/ApparentPower # power faktor (cos phi)
            if ApparentPower>ActivePower:
                reactivePower = math.sqrt(math.pow(ApparentPower,2)-math.pow(ActivePower,2))
            else:
                reactivePower = 0
             
            energyH.append(energy)
            energy = round(sum(energyH)/len(energyH),2)
            if len(energyH) == 10:
                energyH.pop(0)
                hourEnergy = energy*60
            else:
                hourEnergy = energy*60 
            
            waveformVolt.append(volt)
            waveforCurrent.append(current)
            
            if len(waveformVolt) == 100 :  
                waveformVolt.pop(0)
            if len(waveforCurrent) == 100 : 
                waveforCurrent.pop(0)
            
            if powerf < 0.85:
                alertPf = "power faktor bermasalah power factor saat ini : "+'{:.2f}'.format(powerf)
            else:
                alertPf = "power faktor normal"
            if hourEnergy > 6500:
                alertEnergy = "penggunaan Energy berlebih"
            else:
                alertEnergy = "penggunaan Energy stabil"
            if ambienceTemperature > 45:
                alertAmbience = "suhu tinggi pada panel suhu : "+"{:.2f} C".format(ambienceTemperature)
            else:
                alertAmbience = "suhu pada panel stabil"
            if jointTemperature > 45:
                alertJoint = "suhu tinggi pada titik sambung suhu : "+"{:.2f} C".format(jointTemperature)
            else:
                alertJoint = "suhu pada titik sambung stabil"
            
            data_json = {
                'data':[
                    {
                        "data_"+topic:{
                            "Energy":'{:.2f} Wh'.format(hourEnergy),
                            "Voltage":'{:.2f} V'.format(volt),
                            "Current":'{:.2f} A'.format(current),
                            "ActivePower":'{:.2f} W'.format(ActivePower),
                            "ApparentPower":'{:.2f} VA'.format(ApparentPower),
                            "ReactivePower":'{:.2f} VAr'.format(reactivePower),
                            "PowerFactor":'{:.2f}'.format(powerf),
                            "StaeadyStateVolt":waveformVolt,
                            "StaeadyStateCurrent":waveforCurrent,
                            "RawVoltage":"-",
                            "RawCurrent":"-",
                            "TotalHarmonicDistortion":"{:.1f} hz".format(frekuensi),
                            "AmbienceTemperature":"{:.2f} C".format(jointTemperature),
                            "JointTemperature":"{:.2f} C".format(ambienceTemperature)
                        }
                    }
                ],
                'messages':[
                    {   
                        "message_"+topic:{
                            "alertPf":alertPf,
                            "alertEnergy":alertEnergy,
                            "alertAmbience":alertAmbience,
                            "alertJoint":alertJoint,
                        }
                    }
                ]
            }
            dataJson = json.dumps(data_json)
            client.publish('hasil',dataJson)
    
energyH = []
waveformVolt = []
waveforCurrent = []

client.set_callback(sub_cb)
client.subscribe(b'room_1')

while True:
  client.check_msg()
