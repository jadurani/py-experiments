import os, sys
import logging
from time import gmtime

name = 'rsudp_test'

log_dir = os.path.abspath('/tmp/rsudp_test')
log_name = 'rsudp_test.log'
log_loc = os.path.join(log_dir, log_name)
os.makedirs(log_dir, exist_ok=True)


# formatter settings
logging.Formatter.converter = gmtime
LOG = logging.getLogger('main')
LOGFORMAT = '%(asctime)-15s %(msg)s'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

output_dir = False
data_dir = False
scap_dir = False
sound_dir = False
ms_path = False

COLOR = {
	'purple': '\033[95m',
	'blue': '\033[94m',
	'green': '\033[92m',
	'yellow': '\033[93m',
	'red': '\033[91m',
	'white': '\033[0m',
	'bold': "\033[1m"
}


def make_colors_friendly():
	'''
	Makes colors Windows-friendly if necessary.
	'''
	global COLOR
	if os.name == 'posix':
		pass	# terminal colors will work in this case
	else:
		for color in COLOR:
			COLOR[color] = ''

make_colors_friendly()


def printM(msg, sender='', announce=False, color=None):
	'''
	Prints messages with datetime stamp and sends their output to the logging handlers.

	:param str msg: message to log
	:param str sender: the name of the class or function sending the message
	'''
	msg = u'[%s] %s' % (sender, msg) if sender != '' else msg
	if color in COLOR:
		msg = COLOR[color] + msg + COLOR['white']

	# strip emoji from unicode by converting to ascii
	msg = msg.encode('ascii', 'ignore').decode('ascii')
	LOG.info(msg)


def printW(msg, sender='', announce=True, spaces=False):
	'''
	Prints warnings with datetime stamp and sends their output to the logging handlers.

	:param str msg: message to log
	:param str sender: the name of the class or function sending the message
	:param bool announce: whether or not to display "WARNING" before the message
	:param bool spaces: whether or not to display formatting spaces before the message
	'''
	if spaces:
		announce = False

	if announce:
		msg = u'[%s] WARNING: %s' % (sender, msg) if sender != '' else msg
	else:
		if spaces:
			msg = u'[%s]          %s' % (sender, msg) if sender != '' else msg
		else:
			msg = u'[%s] %s' % (sender, msg) if sender != '' else msg
	# strip emoji from unicode by converting to ascii
	msg = msg.encode('ascii', 'ignore').decode('ascii')
	LOG.warning(msg)


def printE(msg, sender='', announce=True, spaces=False):
	'''
	Prints errors with datetime stamp and sends their output to the logging handlers.

	:param str msg: message to log
	:param str sender: the name of the class or function sending the message
	:param bool announce: whether or not to display "WARNING" before the message
	:param bool spaces: whether or not to display formatting spaces before the message
	'''
	if spaces:
		announce = False

	if announce:
		msg = u'[%s] ERROR: %s' % (sender, msg) if sender != '' else msg
	else:
		if spaces:
			msg = u'[%s]        %s' % (sender, msg) if sender != '' else msg
		else:
			msg = u'[%s] %s' % (sender, msg) if sender != '' else msg
	# strip emoji from unicode by converting to ascii
	msg = msg.encode('ascii', 'ignore').decode('ascii')
	LOG.error(msg)
