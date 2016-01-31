#!/usr/bin/python

import Adafruit_DHT
import paho.mqtt.client as mqtt
import json

# Sensor should be set to Adafruit_DHT.DHT11
sensor = Adafruit_DHT.DHT11
sensor_id = 1

# Example using a Raspberry Pi with DHT sensor
# connected to GPIO23.
sensor_pin = 23

# MQTT client set up
mqtt_broker_adress = "m20.cloudmqtt.com"
mqtt_broket_port = 12753

mqttClient = mqtt.Client()
mqttClient_username = "jxhnfzti"
mqttClient_password = "feCowLGfSWA7"

mqttClient.username_pw_set(mqttClient_username, mqttClient_password)
mqttClient.connect(mqtt_broker_adress, port=mqtt_broket_port, keepalive=60, bind_address="")

# Try to grab a sensor reading. Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).  
# If this happens try again!
if humidity is not None and temperature is not None:
	temp_fmt = '{0:0.1f}'.format(temperature)
	hum_fmt = '{0:0.1f}'.format(humidity)
	print 'Temp=%s*C  Humidity=%s%%' % (temp_fmt, hum_fmt)
	
	# publish data to broker
	data = json.dumps({"sensor_id": sensor_id, "temperature": temp_fmt, "humidity": hum_fmt})
	if mqttClient.publish("rasp_sensor", data):
		print "Data published to broker: " + str(data)
	else:
		print "Failed to publish data to broker"
else:
	print 'Failed to get reading. Try again!'
