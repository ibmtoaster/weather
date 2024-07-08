#https://gist.github.com/emxsys/a507f3cad928e66f6410e7ac28e2990f
#weather.service

from RPLCD.i2c import CharLCD
import threading
from time import sleep, asctime
from host import hostname, ip_address, ip_address2
from itertools import cycle

from cpu_temp import get_cpu_temperature2
from weather import weather

myweather = weather()
print('updateTime:', myweather.updateTime())
print('temperature:', myweather.temperature())
print('shortForecast:', myweather.shortForecast())
print('detailedForecast:', myweather.detailedForecast())
print('windSpeed:', myweather.windSpeed())
print('windDirection:', myweather.windDirection())
degreeChar = (
  0b00110,
  0b01001,
  0b01001,
  0b00110,
  0b00000,
  0b00000,
  0b00000,
  0b00000,
)

lock = threading.Lock()

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=4, dotsize=8)
lcd.create_char(0, degreeChar)
display_time = True
lcd.clear()

def display_asctime_line4():
    global display_time
    if display_time == True:
        lock.acquire()
        lcd.cursor_pos = (3,0)
        lcd.write_string(asctime()[0:20])
        lock.release()
    t = threading.Timer(1, display_asctime_line4)
    t.daemon = True
    t.start()

def display_ip_cpu():
        global display_time
        display_time = True
        cpu_temp = "CPU Temp:" + str(get_cpu_temperature2())
        lock.acquire()
        lcd.clear()
        lcd.cursor_pos = (0,0)
        lcd.write_string("Hostname: " + hostname)  # Write line of text to first line of display
        lcd.cursor_pos = (1,0)
        lcd.write_string(ip_address)  # Write line of text to second line of display
        lcd.cursor_pos = (2,0)
        lcd.write_string(cpu_temp)  # Write line of text to first line of display
        lcd.write_string(chr(0))
        lcd.write_string('C')
        lcd.cursor_pos = (3,0)
        lcd.write_string(asctime()[0:20])  # Write line of text to second line of display
        lock.release()

def display_weather():
        global display_time
        display_time = False
        lock.acquire()
        lcd.clear()
        lcd.cursor_pos = (0,0)
        lcd.write_string("Spicewood TX Weather")
        lcd.cursor_pos = (1,0)
        lcd.write_string(myweather.temperature())
        lcd.write_string(chr(0))
        lcd.write_string(myweather.temperatureUnit())
        lcd.write_string(' ==> ')
        lcd.write_string(myweather.temperature_next())
        lcd.write_string(chr(0))
        lcd.write_string(myweather.temperatureUnit())       
        lcd.cursor_pos = (2,0)
        lcd.write_string(myweather.shortForecast())
        if (len(myweather.shortForecast()) <= 20):
          lcd.cursor_pos = (3,0)
        else:
          lcd.write_string(' ')
        lcd.write_string(myweather.windSpeed() + ' ' + myweather.windDirection())
        lock.release()

display_funs = [display_ip_cpu, display_weather]
funs = cycle(display_funs)

def main_display():
    next(funs)()
    t = threading.Timer(10, main_display)
    t.daemon = True
    t.start()

main_display()
display_asctime_line4()

    

