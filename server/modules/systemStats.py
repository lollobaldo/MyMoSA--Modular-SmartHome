import configparser
import json, time
import psutil
from utils import my_logger, execute_every, db_insert

config = configparser.RawConfigParser()
config.read('config.ini')

PRGM_LOGGING_CHANNEL = config.get('MAIN', 'prgm_logging_channel')

PROBING_INTERVAL       = config.getint('SYSTEMSTATS','probing_interval')
MODULE_LOGGING_CHANNEL = config.get('SYSTEMSTATS', 'module_logging_channel')
DATA_OUTPUT_CHANNEL    = config.get('SYSTEMSTATS', 'data_output_channel')

def probe_RPi():
	#p = psutil.Process()
	cpu = psutil.cpu_percent()

	#memory data
	mem = psutil.virtual_memory()
	# Divide from Bytes -> KB
	mem_avail = round(mem.available/1024.0,1)
	mem_tot = round(mem.total/1024.0,1)
	mem_perc = mem.percent

	#disk data
	disk = psutil.disk_usage('/')
	# Divide from Bytes -> KB -> MB -> GB
	disk_free = round(disk.free/1024.0/1024.0/1024.0,1)
	disk_tot = round(disk.total/1024.0/1024.0/1024.0,1)
	disk_perc = disk.percent

	#network data
	net = psutil.net_io_counters()
	# Divide from Bytes -> KB
	net_sent = round(net.bytes_sent/1024.0,1)
	net_recv = round(net.bytes_recv/1024.0,1)

	net_ip = psutil.net_if_addrs()['wlan0'][0].address

	temp = int(open("/sys/class/thermal/thermal_zone0/temp").readline())/1000

	#cpu data
	#cpu = psutil.cpu_percent(percpu=True)

	# a Python object (dict):
	json_data = {
		"date": int(time.time()*1000.0),
		"cpu": str(cpu),
		"mem_avail": mem_avail,
		#"mem_tot": mem_tot,
		#"mem_perc": mem_perc,
		"disk_free": disk_free,
		#"disk_tot": disk_tot,
		#"disk_perc": disk_perc,
		"net_sent": net_sent,
		"net_recv": net_recv,
		#"net_ip":net_ip,
		"temp": temp
	}

	json_to_send = json.dumps(json_data)
	my_logger(mqtt_client , MODULE_LOGGING_CHANNEL , "New system stats probed - " + json_to_send)
	mqtt_client.publish(DATA_OUTPUT_CHANNEL , json_to_send , 2 , False)
	db_insert('''INSERT INTO systemStats(date, cpu, mem_avail, disk_free, net_sent, net_recv, temp)
		VALUES(:date,:cpu,:mem_avail,:disk_free,:net_sent,:net_recv,:temp)''' , json_data)
	#cursor.execute('''CREATE TABLE systemStats(date INTEGER PRIMARY KEY, cpu TEXT, mem_avail INTEGER, disk_free INTEGER, net_sent REAL, net_recv REAL, temp REAL)''')

def cleanup():
	my_logger(mqtt_client , MODULE_LOGGING_CHANNEL , "SystemStats cleaned up, ready to kill")

TO_SUBSCRIBE = {}
def setup(client):
	global mqtt_client
	mqtt_client = client
	execute_every(probe_RPi , PROBING_INTERVAL)
	my_logger(mqtt_client , PRGM_LOGGING_CHANNEL , "SystemStats module loaded")
