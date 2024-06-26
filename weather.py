import requests
import json
import threading

#The API endpoint
#url = "https://api.weather.gov/zones/forecast/TXZ192"
#forecast_url = "https://api.weather.gov/gridpoints/EWX/145,95/forecast"
#mylocation_url = "https://api.weather.gov/points/30.3661,-98.0266"
#hourly_url = "https://api.weather.gov/gridpoints/EWX/145,95/forecast/hourly"

hourly_url = "https://api.weather.gov/gridpoints/EWX/145,95/forecast/hourly"

class weather :
    def __init__(self, url=hourly_url, updateInterval=1800):
        self.url = url
        self.updateInterval = updateInterval
        self.json = {}
        self.current = []
        self.update()
        
    def update(self):
        response = requests.get(self.url)
        self.json = response.json()
        self.current = self.json.get('properties')['periods'][0]
        print('weather.update:' + self.updateTime())
        threading.Timer(self.updateInterval, self.update).start()

    def dump(self):
        print(self.json)
 
    def updateTime(self):
       return self.json.get('properties')['updateTime']
        
    def temperature(self):
        #return self.json.get('properties')['periods'][0]['temperature']
        return str(self.current['temperature']) + ' ' + self.current['temperatureUnit']
 
    def shortForecast(self):
       return self.current['shortForecast']

    def detailedForecast(self):
       return self.current['detailedForecast']

    def windSpeed(self):
       return self.current['windSpeed']

    def windDirection(self):
       return self.current['windDirection']

if __name__ == '__main__':     
  myweather = weather()
  #myweather.dump()
  print('updateTime:', myweather.updateTime())
  print('temperature:', myweather.temperature())
  print('shortForecast:', myweather.shortForecast())
  print('detailedForecast:', myweather.detailedForecast())
  print('windSpeed:', myweather.windSpeed())
  print('windDirection:', myweather.windDirection())
        

