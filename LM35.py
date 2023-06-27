import machine,time

# Konfigurasi pin ADC
adc = machine.ADC(machine.Pin(34))  # Ganti dengan pin yang sesuai
adc.atten(machine.ADC.ATTN_11DB)  # Konfigurasi pengaturan tegangan referensi

# Fungsi untuk membaca suhu dari sensor LM35
def read_lm35_temperature():
    reading = adc.read()  # Baca nilai ADC
    voltage = reading * 3.3 / 4095  # Konversi nilai ADC ke tegangan
    temperature = voltage * 100  # Konversi tegangan menjadi suhu dalam derajat Celsius
    return temperature

# Membaca dan mencetak suhu dari sensor LM35
while True:
  temperature = read_lm35_temperature()
  print("Suhu: {} derajat Celsius".format(temperature))
  time.sleep(2)


