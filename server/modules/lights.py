import configparser
#import os, socket
import RPi.GPIO as GPIO  # pylint: disable=fixme, E0611, E0401 --dev
import paho.mqtt.client as mqtt
from utils import my_logger

config = configparser.RawConfigParser()
config.read('config.ini')

PRGM_LOGGING_CHANNEL = config['MAIN']['prgm_logging_channel']

MODULE_LOGGING_CHANNEL = config.get("LIGHT0", "module_logging_channel")
DATA_INPUT_CHANNEL     = config.get("LIGHT0", "data_input_channel")
DATA_PIN               = config.getint('LIGHT0','data_pin')

#execute command - looks complicated because I will implement colours / strobes
def new_command(command):
	if (command == "on"):
		GPIO.output(DATA_PIN, GPIO.HIGH)
		my_logger(mqtt_client , MODULE_LOGGING_CHANNEL , "Turning light 0 on")
	elif (command == "off"):
		GPIO.output(DATA_PIN, GPIO.LOW)
		my_logger(mqtt_client , MODULE_LOGGING_CHANNEL , "Turning light 0 off")

#cleanup needed for GPIO
def cleanup():
	GPIO.cleanup()
	my_logger(mqtt_client , MODULE_LOGGING_CHANNEL , "Lights cleaned up, ready to kill")

TO_SUBSCRIBE = {DATA_INPUT_CHANNEL: new_command}
def setup(client):
	global mqtt_client
	mqtt_client = client
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(DATA_PIN, GPIO.OUT)
	my_logger(mqtt_client , PRGM_LOGGING_CHANNEL , "Lights module loaded")