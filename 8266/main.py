#dependecies
import machine, time, os, network, socket, math, dht, ujson, urequests
# This out will be converted to JSON to send to the server
out={'f':False,'t':False,'temp':0,'humid':0}
#74hc595 relay latch
clk=machine.Pin(12,machine.Pin.OUT)
ds=machine.Pin(0, machine.Pin.OUT)
lch=machine.Pin(13, machine.Pin.OUT)
#--
# to get value from fire sensor
fire=machine.Pin(14, machine.Pin.IN)
# to get value from dht11 temperature sensor
d = dht.DHT11(machine.Pin(16))
# to send signal to buzzer
buzz=machine.Pin(5, machine.Pin.OUT)
# to get value form PIR sensor
pir=machine.Pin(4, machine.Pin.IN)

# open.json file contain received values from server
jsn=open('config.json')
# to convert value to object
jsn.seek(0)
config=ujson.loads(jsn.read())
jsn.close()

# this list represent the value of s0-s3 mapped according to index value
s=[0,0,0,0]

# update function to update device status according to received value
def update():
    d.measure()
    jsn=open('config.json')
    jsn.seek(0)
    config=ujson.loads(jsn.read())
    jsn.close()
    s[0]=int(config['s0'])
    s[1]=int(config['s1'])
    s[2]=int(config['s2'])
    s[3]=int(config['s3'])
    rpush(s)
    out["temp"]=d.temperature()
    out['humid']=d.humidity()

# to get json from server
def get():
    fdata=urequests.get('http://litfur.herokuapp.com/')
    time.sleep_ms(50)
    if fdata.text:
        print('fdata:'+fdata.text)
        jsn=open('config.json','w')
        jsn.write(fdata.text)
        jsn.close()

# to post information like temparture and humidity to server
def post():
    res = urequests.post('http://litfur.herokuapp.com/post', headers = {'content-type': 'application/json'}, data = ujson.dumps(out))

# to check if there is an emergency
def isemrgcy():
    if isFire():
        out['f']=True
        rpush([1,1,1,1])
        return True

    if config['l']:
        if isTheft():
            out['t']=True
            rpush([0,0,0,0])
            return True
    return False
# check file emergency
def isFire():
    for i in range(10):
        if(fire.value()==0):
            return True
        time.sleep_ms(50)
    return False
#check theft emergency
def isTheft():
    for i in range(10):
        if(pir.value()==1):
            return True
        time.sleep_ms(50)
    return False
# to trigger buzzer
def buzzer():
    for i in range(80):
        buzz.value(1)
        time.sleep_ms(1)
        buzz.value(0)
        time.sleep_ms(1)
    time.sleep_ms(50)
    for i in range(50):
        buzz.value(1)
        time.sleep_ms(2)
        buzz.value(0)
        time.sleep_ms(2)

#to update switches is push s0-s03 list to 74hc595 serially
def rpush(arr):
    rarr=[0,0,0,int(arr[3]),int(arr[2]),int(arr[1]),int(arr[0]),0] #000 s3 s2 s1 s0 0
    clk.off()
    lch.off()
    ds.off()
    for i in rarr:
        ds.value(i)
        clk.on()
        clk.off()
    clk.off()
    lch.on()
    lch.off()

# sequence of the device
while 1:
    if not isemrgcy():
        get()
        update()
        post()
    else:
        while 1:
            buzzer()
            post()
            buzzer()
            get()
            buzzer()
            jsn=open('config.json')
            jsn.seek(0)
            config=ujson.loads(jsn.read())
            jsn.close()
            buzzer()
            if config['r']:
                break

