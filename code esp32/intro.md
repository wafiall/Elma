# program explanation
esp32 using micropython
### 1. The first program that will be executed by esp32 is ' boot.py '
in the program ' boot.py ' there is code to create json file 
1. 'datassid_default' which contains ssid and password which works to set esp32 network name
2. 'datakey_default' which contains the name esp32, broker, and topic receiver which functions to connect mqtt

but if your esp32 not connected to wifi, esp32 will starting the configuration portal in default link is' 192.168.4.1 '.
The configuration portal is useful for setting up wifi networks, esp32 names, esp32 passwords, receiver topic, broker name.
when everything is finished setting up and the wifi is successfully connected, the program will execute ' active.py '

### 2. Program running on ' active.py '
When the 'active.py' program starts running, the sensors also start functioning, and the received data is first stored in JSON format and then sent via the MQTT protocol to the pre-established topic. The sensors included in the program are:

1. PZEM-004T
   This sensor is used to measure electrical parameters such as voltage (V), current (A), active power (W), energy (kWh), power factor (PF), and frequency (Hz). It is commonly used to monitor power consumption in electrical appliances or energy systems.
2. LM35
   This sensor is used to measure temperature in Celsius scale. It is often utilized in various applications, including indoor temperature monitoring, electronic devices, and temperature control systems.
