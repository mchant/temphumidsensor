from umqtt.simple import MQTTClient
from machine import Pin, RTC, deepsleep
from dht import DHT11
import time
import credentials

d = DHT11(Pin(2))

def deep_sleep(msecs):
  #configure RTC.ALARM0 to be able to wake the device
  rtc = RTC()
  rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
  # set RTC.ALARM0 to fire after Xmilliseconds, waking the device
  rtc.alarm(rtc.ALARM0, msecs)
  #put the device to sleep
  deepsleep()

def get_temp():
    d.measure()
    temperature = d.temperature() * 9 / 5 + 32
    temperature *= 0.9  # because it's not accurate
    return temperature, d.humidity()

def main(server=credentials.server):
    while True:
        c = MQTTClient("umqtt_client", server)
        c.user = credentials.user
        c.pswd = credentials.pswd
        c.connect()
        temp, humi = get_temp()
        c.publish(credentials.temperature_address, b"{}".format(temp))
        c.publish(credentials.humidity_address, b"{}".format(humi))
        c.disconnect()
        time.sleep(60)

if __name__ == "__main__":
    main()
