import machine
import time

# Konfigurasi pin TX dan RX
uart = machine.UART(1, baudrate=9600, tx=17, rx=16)

# Fungsi untuk membaca data dari modul PZEM
def read_pzem_data():
    uart.write(b'\xB0\xC0\xA8\x01\x01\x01\x01\x01\x01\x01\x01\xFE')
    time.sleep(0.5)  # Tunggu respon dari modul PZEM
    response = uart.read(7)
    voltage = (response[1] << 8 | response[2]) / 10.0
    current = (response[3] << 8 | response[4]) / 100.0
    power = response[5] << 8 | response[6]
    return voltage, current, power

read_pzem_data()
