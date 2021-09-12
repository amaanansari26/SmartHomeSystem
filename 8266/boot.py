#dependencies
import machine, time, os, network, socket, math, dht, ujson

# to read config.json, if config.json doesnt exit it will create one with default values
filelist=os.listdir()
if 'config.json' not in filelist:
    jsn=open('config.json','w')
    jsn.write('{"s0":false,"s1":false,"s2":false,"s3":false,"l":false,"r":false}')
    jsn.close()

# wifi.json contain default wifi informations
if 'wific.json' not in filelist:
    wific=open('wific.json','w')
    wific.write('{"SSID":"Amaan","PASS":"myWifiPassword"}')
    wific.close()
wific=open('wific.json')
wific.seek(0)
wific=ujson.loads(wific.read())
# turnon wifi
network.WLAN(network.AP_IF).active(False)
sta = network.WLAN(network.STA_IF)
sta.active(True)
#pass value to wifi module
sta.connect(wific['SSID'],wific['PASS'])
while(not sta.isconnected()):
    print('connecting...')
