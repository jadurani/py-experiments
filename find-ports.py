import serial.tools.list_ports

def find_arduino_port():
  '''
  Find the serial port of the connected Arduino board.
  '''
  ports = list(serial.tools.list_ports.comports())
  for p in ports:
    print('\n>>>>>> PORT ITEM <<<<<<<')
    print('device: ', p.device) # The name of the device associated with the port (e.g., /dev/ttyUSB0 or COM3).
    print('name: ', p.name) # The name of the port.
    print('description: ', p.description) # A description of the port.
    print('manufacturer: ', p.manufacturer) # The manufacturer of the port.
    print('hwid: ', p.hwid) # The hardware ID of the port.
    print('interface: ', p.interface) # The interface type of the port.

    if 'Arduino' in p.description or 'Arduino' in str(p.manufacturer):
      print('>>>>>>>>>>>>>>>>>> Found arduino port %s' % p.device)
      return p.device
  print('\n\nEND OF PORT LIST: Unable to find arduino port')
  return None

port = find_arduino_port()
print(port)