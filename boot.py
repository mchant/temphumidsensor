import time
import ubinascii
import machine
import micropython
import network
import esp
import credentials
esp.osdebug(None)
import gc
gc.collect()

ssid = credentials.ssid
password = credentials.password
mqtt_server = credentials.mqtt_server
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'sensors'

last_message = 0
message_interval = 15
counter = 0

station = network.WLAN(network.STA_IF)
station.ifconfig(('192.168.1.201', '255.255.255.0', '192.168.1.1', '192.168.1.1'))

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())