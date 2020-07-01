import micropython
micropython.alloc_emergency_exception_buf(100)


from machine import Timer



def syncTime():
    from ntptime import settime
    try:
        settime()
    except:
        pass

timSyncTime = Timer(-1)
# tim.init(period=5000, mode=Timer.ONE_SHOT, callback=lambda t:print(1))
timSyncTime.init(period=1000 * 60 * 1, mode=Timer.PERIODIC, callback=lambda t:syncTime())

# ---

import network

wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
# wlan.scan()             # scan for access points
# wlan.isconnected()      # check if the station is connected to an AP
wlan.connect('VM910566-2G', 'K@ramb0lsk!') # connect to an AP
# wlan.config('mac')      # get the interface's MAC address
# wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses

# ap = network.WLAN(network.AP_IF) # create access-point interface
# ap.config(essid='ESP-AP') # set the ESSID of the access point
# # ap.config(max_clients=10) # set how many clients can connect to the network
# ap.active(True)         # activate the interface

# time.sleep(1)

###############################

import machine, neopixel

nph = neopixel.NeoPixel(machine.Pin(12), 24)
npm = neopixel.NeoPixel(machine.Pin(14), 24)


#########
clMin = (0,2,0)
clMout = (0,0,0)

def onMin(m):
    hin = round(m * 24 / 60)
    for i in range(hin):
        npm[i] = clMin

def onMout(m):
    hin = round(m * 24 / 60)
    for i in range(hin, 24):
        npm[i] = clMout

def onM(h): 
    onMin(h)
    onMout(h)
    npm.write()

def offM():
    for i in range(24):
        npm[i] = (0, 0, 0)
    npm.write();



#########
clHin = (3,0,0)
clHout = (0,0,0)

def onHin(h):
    for i in range(h):
        nph[i] = clHin

def onHout(h):
    for i in range(h, 12):
        nph[i] = clHout

def onH(h): 
    # h = (hh + 6) % 12
    onHin(h)
    onHout(h)
    nph.write()

def offH():
    for i in range(12):
        nph[i] = (0, 0, 0)
    nph.write();

def offHM(): 
    offH()
    offM()

#################
from math import ceil

def doShowHr(hr, ind, nph):
    # if hr == 0 : hr = 12
    offset = 2
    l = 0 + offset
    r = hr + offset
    if (ind >= l) and (ind < r):
        nph[ind] = (2,0,0)
    else:
        nph[ind] = (0,0,0)

def doShowMn(mn, ind, nph):
    if mn == 0: mn = 60
    offset = -1
    dind = ceil(ind * 2.5) 
    l = 0 + offset 
    r = mn + offset
    if (dind >= l) and (dind <= r):
        npm[ind] = (0,2,4)
    else:
        npm[ind] = (0,0,0)

def showH(hr):
    for i in range(12):
        doShowHr(hr,i, nph)
    nph.write()

def showM(mn):
    for i in range(24):
        doShowMn(mn, i, npm)
    npm.write()

#################

import utime
import time

def showTime():
    secs = utime.time()    
    (yy,mt,dd,hr,mn,s,zz,zzz) = utime.localtime(secs)
    # mn += 1
    hr += 1
    hr %= 12
    mn %= 60
    if (s % 10 == 0):
        print("Hour:")
        print(hr)
        print("Minute:")
        print(mn)
    showH(hr)
    showM(mn)

timShowTime = Timer(-1)
timShowTime.init(period=(1000 * 3), mode=Timer.PERIODIC, callback=lambda t:showTime())


# while (True):
#     showTime()
#     time.sleep(1)
# timShowTime.deinit()