from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt
import json


def connect(client, userdata, flags, rc):  # rc = return code if 1 = error
    if rc == 0:
        rc = "success"
    else:
        rc = "error"
    print("Connected to mqtt "+str(rc))
    client.subscribe("gateway")


def message(client, userdata, msg):
    key = '7C7nMN_-ShTaSBOzZL4DWC66slvIYL9xUzeDiNIQ3Gg='
    fernet = Fernet(key)
    decrypt = fernet.decrypt(msg.payload)
    pesanx = decrypt.decode('utf-8')
    pesan = json.loads(pesanx)
    print(pesan)
    pub = (pesan['pub'])
    powerf = float(pesan['PowerFactor'])
    hourEnergy = float(pesan['HourEnergy'])
    ambienceTemperature = float(pesan['AmbienceTemperature'])
    joinTemperature = float(pesan['JoinTemperature'])

    if powerf < 0.85:
        alertPowerfactor = 1
    else:
        alertPowerfactor = 0
    if hourEnergy > 6500:
        alertEnergy = 1
    else:
        alertEnergy = 0
    if ambienceTemperature > 45:
        alertAmbience = 1
    else:
        alertAmbience = 0
    if joinTemperature > 45:
        alertJoint = 1
    else:
        alertJoint = 0

    data_alert = {
        'alertpf': alertPowerfactor,
        'alerthe': alertEnergy,
        'alertat': alertAmbience,
        'alertjt': alertJoint
    }
    alert = json.dumps(data_alert)
    client.publish(pub, alert)
#     # print(msg.payload)


client = mqtt.Client()
client.username_pw_set('median', 'median2022')
client.on_connect = connect
client.on_message = message

client.connect('157.245.192.125')
client.loop_forever()
