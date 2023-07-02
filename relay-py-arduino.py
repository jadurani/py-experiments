import serial.tools.list_ports
import sys
import time

BAUD_RATE = 9600
IOT_KEYWORDS = ['Arduino', 'Silicon Labs']

def find_arduino_port():
	'''
	Find the serial port of the connected Arduino board.
	'''
	print('Finding serial port to connect Arduino unit...')

	ports = list(serial.tools.list_ports.comports())
	for p in ports:
		for keyword in IOT_KEYWORDS:
			if keyword in p.description or keyword in str(p.manufacturer):
				print('Found arduino port %s' % p.device)
				return p.device

	print('Unable to find arduino port')
	raise ValueError('No arduino port found!')

def _start_connection():
	try:
		print('Opening serial connection...')
		ser = serial.Serial(arduino_port, BAUD_RATE)
		print('Serial connection opened!')
		return ser
	except Exception as e:
		print('Failed to open serial connection: ' + str(e))
		alive = False
		sys.exit()

def _handle_close():
	print('Closing serial connection...')
	ser.close()

def _send_signal(signal):
	print('Sending signal: %s' % signal)
	ser.write(b'%s' % bytes(signal, 'utf-8'))

def run():
	start_time = time.time()
	HIGH_SENT = False
	LOW_SENT = False
	while time.time() - start_time < 10:
		# AFTER 2 seconds, send a high signal
		if time.time() - start_time > 2 and not HIGH_SENT:
			_send_signal('HIGH')
			HIGH_SENT = True

		# after 8 seconds, send a low signal
		if time.time() - start_time > 8 and not LOW_SENT:
			_send_signal('LOW')
			LOW_SENT = True

		# this should read all messages
		if ser.in_waiting > 0:
			data = ser.readline().decode().strip()
			print(f"Received from Arduino: {data}")

	_send_signal('LOW')
	_handle_close()
	print('Exiting...')
	sys.exit()

arduino_port = find_arduino_port()
ser = _start_connection()
run()
