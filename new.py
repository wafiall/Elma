import uPZEM_004t,time

test=uPZEM_004t.uPZEM(1,pins=[17,16])

while True:
  print(test.read_input_registers(1))
  time.sleep(2)

