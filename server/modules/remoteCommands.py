import configparser
import os, socket
import paho.mqtt.client as mqtt
from utils import my_logger

config = configparser.RawConfigParser()
config.read('config.ini')

PRGM_LOGGING_CHANNEL = config.get('MAIN', 'prgm_logging_channel')

MODULE_LOGGING_CHANNEL = config.get("REMOTECOMMANDS", "module_logging_channel")
DATA_INPUT_CHANNEL     = config.get("REMOTECOMMANDS", "data_input_channel")
DATA_OUTPUT_CHANNEL    = config.get("REMOTECOMMANDS", "data_output_channel")

#get external ip address - idk found on stackoverflow
def getIp():
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s: 
		s.connect(("google.com", 80))
		return s.getsockname()[0]

def reboot():
	os.system("sudo reboot +1")
	return("Reboot successful")

def shutdown():
	os.system("sudo shutdown +1")
	return("Shutdown successful")

def execute_command(command):
	return "function not implemented yet"

def new_command(command):
	my_logger(mqtt_client , MODULE_LOGGING_CHANNEL , "Executing: " + command)
	known_commands = {
		"getip":    getIp,
		"reboot":   reboot,
		"shutdown": shutdown,
	}
	# Get the function from switcher dictionary
	func = str(known_commands.get(command.lower(), lambda: execute_command(command))())
	# Execute the function
	my_logger(mqtt_client , MODULE_LOGGING_CHANNEL , "Executed: " + command + ", returned: " + func)
	mqtt_client.publish(DATA_OUTPUT_CHANNEL , func , 2 , False)

def cleanup():
	my_logger(mqtt_client , MODULE_LOGGING_CHANNEL , "RemoteCommands cleaned up, ready to kill")

TO_SUBSCRIBE = {DATA_INPUT_CHANNEL: new_command}
def setup(client):
	global mqtt_client
	mqtt_client = client
	my_logger(mqtt_client , PRGM_LOGGING_CHANNEL , "RemoteCommands module loaded")