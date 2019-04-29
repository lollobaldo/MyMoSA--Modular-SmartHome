import configparser
import json, time
import Adafruit_DHT as DHT  # pylint: disable=fixme, E0401 --dev
from utils import my_logger, execute_every, db_insert

config = configparser.RawConfigParser()
config.read("config.ini")


PRGM_LOGGING_CHANNEL = config.get("MAIN", "prgm_logging_channel")

PROBING_INTERVAL       = config.getint("DHT","probing_interval")
MODULE_LOGGING_CHANNEL = config.get("DHT", "module_logging_channel")
DATA_OUTPUT_CHANNEL    = config.get("DHT", "data_output_channel")
DATA_PIN               = config.getint("DHT","data_pin")

dht11_sensor = DHT.DHT11

def probe_DHT():
	
	#probe sensor
	humidity, temperature = int(DHT.read_retry(dht11_sensor, DATA_PIN))
	#convert float to int - don"t need decimal points
	humidity = int(humidity)
	temperature = int(temperature)

	my_logger(mqtt_client , MODULE_LOGGING_CHANNEL , "New DHT data probed - Temperature: {0:d} C ; Humidity: {1:d} %".format(temperature, humidity))
	json_data = {
		"date": int(time.time()*1000.0),
		"humidity": humidity,
		"temperature": temperature
	}
	json_to_send = json.dumps(json_data)
	
	#send data
	mqtt_client.publish(DATA_OUTPUT_CHANNEL , json_to_send , 2 , False)
	db_insert("""INSERT INTO DHT(date, humidity, temperature) VALUES(:date,:humidity,:temperature)""" , json_data)

def cleanup():
	my_logger(mqtt_client , MODULE_LOGGING_CHANNEL , "DHT cleaned up, ready to kill")

TO_SUBSCRIBE = {}
def setup(client):
	global mqtt_client
	mqtt_client = client
	execute_every(probe_DHT , PROBING_INTERVAL)
	my_logger(mqtt_client , PRGM_LOGGING_CHANNEL , "DHT module loaded")