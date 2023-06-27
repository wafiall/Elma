from random import uniform
from Crypto.Cipher import AES
from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt
import math
import json


client = mqtt.Client()
# client.connect("broker.hivemq.com")
client.username_pw_set('median', 'median2022')
client.connect('157.245.192.125')

# key untuk Encrypt pesan yang akan di kirim ke dashboard
EncryptKey = '7C7nMN_-ShTaSBOzZL4DWC66slvIYL9xUzeDiNIQ3Gg='
fernet = Fernet(EncryptKey)

# Key untuk decrypt message dari controller
key = b'\xe5\x82\xe7\xc1\xcfP9\xab\x9e4-(\\}\xab\xaa\xf3\xe2S\x054d\xdf"\x82\xd0\xd8\'\x9ee\xc6\x1b'
iv = b"\xfeYD\x91\xf2\xcd\xf1\xc6\xc9\xd0\x9c#\xf1\xad'\x9a"


def message(client, userdata, msg):
    Message = (msg.payload)
    Cipher = AES.new(key, AES.MODE_CBC, iv)
    DecryptedData = Cipher.decrypt(Message)
    data = json.loads(str(DecryptedData.decode('utf-8').rstrip('\x03')))
    print(data)
    # access the JSON fields
    pub = (data['pub'])
    current = float(data['current'])
    volt = float(data['volt'])
    frekuensi = float(data['frekuensi'])
    ActivePower = float(data['activePower'])
    energy = float(data['energy'])
    ambienceTemperature = float(data['ambienceTemperature'])
    jointTemperature = float(data['jointTemperature'])

    # rumus
    ApparentPower = volt*current  # daya semu(VA)
    powerf = ActivePower/ApparentPower  # power faktor (cos phi)
    # powerf = 0.89
    reactivePower = math.sqrt(
        (math.pow(ApparentPower, 2))-(math.pow(ActivePower, 2)))
    hourEnergy = energy*60

    data = {
        "pub": format(pub),
        "HourEnergy": '{:.2f}'.format(hourEnergy),
        "Voltage": '{:.2f}'.format(volt),
        "Current": '{:.2f}'.format(current),
        "ActivePower": '{:.2f}'.format(ActivePower),
        "ApparentPower": '{:.2f}'.format(ApparentPower),
        "ReactivePower": '{:.2f}'.format(reactivePower),
        "PowerFactor": '{:.2f}'.format(powerf),
        "StaeadyStateVolt": "Normal",
        "StaeadyStateCurrent": "Normal",
        "RawVoltage": "Normal",
        "RawCurrent": "Normal",
        "TotalHarmonicDistortion": "{:.1f} hz".format(frekuensi),
        "AmbienceTemperature": ambienceTemperature,
        "JoinTemperature": jointTemperature
    }
    dataJson = json.dumps(data)
    dataByte = dataJson.encode('utf-8')
    EncryptedData = fernet.encrypt(dataByte)
    client.publish('gateway', EncryptedData)
    # client.publish('gateway', dataJson)
    # print(EncryptedData)
    # print(data)


client.on_message = message
client.subscribe("controller")
client.loop_forever()
