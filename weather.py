import requests
import json
import threading
import time

#The API endpoint
#url = "https://api.weather.gov/zones/forecast/TXZ192"
#forecast_url = "https://api.weather.gov/gridpoints/EWX/145,95/forecast"
#mylocation_url = "https://api.weather.gov/points/30.3661,-98.0266"
#hourly_url = "https://api.weather.gov/gridpoints/EWX/145,95/forecast/hourly"

hourly_url = "https://api.weather.gov/gridpoints/EWX/145,95/forecast/hourly"
header_no_cache = {
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Expires": "0"
}

class weather :
    def __init__(self, hurl=hourly_url, updateInterval=300):
        self.url = hurl
        self.updateInterval = updateInterval
        self.json = {}
        self.current = []
        self.update()
        
    def update(self):
        try:
          nextCall = self.updateInterval
          response = requests.get(self.url, headers=header_no_cache)
          self.json = response.json()
          self.current = self.json.get('properties')['periods'][0]
          self.next = self.json.get('properties')['periods'][1]
          print(time.ctime(),'weather.update:' + self.updateTime(), self.temperature(), self.number())
          #print(self.current)
        except:
          print(time.ctime(),'weather.update exception')
          nextCall = 5
        finally:
          threading.Timer(nextCall, self.update).start()

    def dump(self):
        print(self.json)
 
    def updateTime(self):
       return self.json.get('properties')['updateTime']
        
    def temperature(self):
        #return self.json.get('properties')['periods'][0]['temperature']
        return str(self.current['temperature'])
    
    def temperature_next(self):
        return str(self.next['temperature'])
    
    def temperatureUnit(self):
        return self.current['temperatureUnit']
 
    def shortForecast(self):
       return self.current['shortForecast']

    def detailedForecast(self):
       return self.current['detailedForecast']

    def windSpeed(self):
       return self.current['windSpeed']

    def windDirection(self):
       return self.current['windDirection']
    
    def number(self):
        return self.current['number']

if __name__ == '__main__':     
  myweather = weather()
  #myweather.dump()
  print('updateTime:', myweather.updateTime())
  print('temperature:', myweather.temperature())
  print('shortForecast:', myweather.shortForecast())
  print('detailedForecast:', myweather.detailedForecast())
  print('windSpeed:', myweather.windSpeed())
  print('windDirection:', myweather.windDirection())
  print('number:', myweather.number())
  print('threading.active_count():', threading.active_count())
        

