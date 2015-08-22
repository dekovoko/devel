# -*- coding: utf-8 -*-

# weather code : http://bugs.openweathermap.org/projects/api/wiki/Weather_Condition_Codes
# インターフェースBINDしての通信の仕方: http://docs.python.jp/3/library/socket.html
# python のsocket通信: http://memo.saitodev.com/home/python_network_programing/#select

import json
import sys
from socket import *
from contextlib import closing
import urllib
import urllib2


# - Weather Analyze Def -
def weatherChk(json_data):
  weatherList = { '01':'晴れ','02':'晴れ','03':'曇り','04':'曇り','09':'雨','10':'雨','11':'雷雨','13':'雪','50':'霧','00':'取得不可' }
  max_temp = json_data["main"]["temp_max"]-273.15
  min_temp = json_data["main"]["temp_min"]-273.15
  return weatherList[json_data["weather"][0]["icon"][:2]]


def changeLumpChk(g_weather):
  if g_weather ==  "01" or g_weather == "02" : voice = "hare"
  elif g_weather ==  "03" or g_weather == "04" : voice = "kumori"
  elif g_weather ==  "09" or g_weather == "10" : voice = "ame"
  elif g_weather ==  "11" or g_weather == "13" or g_weather == "50" : voice = "kaminari"
  else : voice = "unknown"

  socket_result = socketDevice(voice)
  return 0


# - Get Internet Resource Def -
def getResource(g_url, g_params):

  if len(g_params) > 0 : request_url = g_url + "?" + urllib.urlencode(g_params)
  else : request_url = g_url

  try:
    response = urllib2.urlopen(request_url)
    return response
  except urllib2.URLError, e:
    print e
    sys.exit(12)


# - Get Internet Resource Def -
def socketDevice(g_voice):

  # TODO: 接続先ホストは、grexxxを拾って埋め込まないと
  host = "127.0.0.1"
  port = 51021
  bufsize = 4096

  client_sock = socket(AF_INET, SOCK_STREAM)
  client_sock.setsockopt(SOL_SOCKET, 25, "lo")
  try:
    with closing(client_sock):
      client_sock.connect((host, port))
      client_sock.send(g_voice)
      print (client_sock.recv(bufsize))
    return 0
      except socket.gaierror ,e:
    print e
    sys.exit(12)


def main():
  params = {'q':'Tokyo'}
  baseurl = 'http://api.openweathermap.org/data/2.5/weather'

  #response = getResource(baseurl, params)
  #json_data = json.loads(response.read().encode("utf-8"))

  # - DEBUG -
  response = '{"coord":{"lon":139.69,"lat":35.69},"sys":{"type":1,"id":7619,"message":0.1151,"country":"JP","sunrise":1418074756,"sunset":1418110074},"weather":[{"id":800,"main":"Clear","description":"Sky is Clear","icon":"01n"}],"base":"cmc stations","main":{"temp":281.28,"pressure":1024,"humidity":37,"temp_min":279.15,"temp_max":283.15},"wind":{"speed":9.3,"deg":340,"gust":14.4},"clouds":{"all":0},"dt":1418119080,"id":1850147,"name":"Tokyo","cod":200}'
  json_data = json.loads(response.encode("utf-8"))
  # ---------

  weather = json_data["weather"][0]["icon"][:2]
  print changeLumpChk(weather)


if __name__ == '__main__':
  main()
