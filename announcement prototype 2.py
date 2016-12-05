#from itertools import cycle, islice, dropwhile
import hackromatics
import math
import time

#For OS X/macOS System Text-to-speech
import os

# a couple sample syncromatics hosted web sites for transit
host = dict(
    losangeles='http://ladotbus.com',           # Los Angeles transit
    penn='http://pennrides.com',                # UPenn transit
    keywest='http://kwtransit.com',             # key west
    ucsd='http://www.ucsdbus.com/',             # UCSD
    usf='http://www.usfbullrunner.com',         # University of South Florida
    presidio='http://www.presidiobus.com/',     # SF Presidio
    longbeach='http://csulbshuttle.com',        # CSU Long Beach
    miss='http://transit.msstate.edu/',         # Mississippi State
    bronco='http://broncoshuttle.com/',         # CSU Ponoma
    delaware='http://udshuttle.com',            # Univ of Delaware
    sandiego='http://usdtram.com',              # Univ of San Diego
    nih='http://wttsshuttle.com/',              # NIH
    ucsf='http://ucsfshuttles.com',             # UCSF
    uci='http://ucishuttles.com'                # UC Irvine
)

# connect to a syncromatics transit web site
site = 'delaware'
api = hackromatics.API(host[site])

# to get info about the transit regions...
regions = api.regions()

# to iterate through all the information you can loop through everything
# in this ugly for loop...

stop_ann = 0

for region in api.regions():
    print ('REGION:', region.ID, region.Name)
region = input('Select region by number: ')
for route in api.routes(region):
    print ('(ID: '+str(route.ID)+')', 'ROUTE:', route.Name)
route = input('Select route by ID: ')
stops = {x.ID:x.Name for x in api.stops(route)}
for veh in api.vehicles(route):
    print ('(ID: '+str(veh.ID)+')', 'VEHICLE:',veh.Name)
vehicle = input('Select vehicle by ID: ')

end = False
fails=0

print ("Now en route!")
print('--')
while True:
    delay = 5;
    try:
        end = True
        
        arrivals = api.vehicle_arrivals(vehicle)
        print([(stops[x.StopID], x.SecondsToArrival) for x in arrivals])
        len_nexts = len(arrivals)
        for i in range(len_nexts):
            fails=0
            if (arrivals[i].SecondsToArrival > 0):
                end = False
                if (arrivals[i].StopID!=stop_ann):
                    if (arrivals[i].SecondsToArrival<=41):
                        #Invoke OS X/macOS System Text-to-speech
                        os.system('say "Now approaching: '
                            + stops[arrivals[i].StopID] + '" &')
                        stop_ann = arrivals[i].StopID
                        print("Now approaching", stops[stop_ann])
                        print('--')
                        delay = 5
                    else:
                        delay = 15
                break
        if end:
            fails+=1
            if fails == 3:
                break
            else:
                delay = 10
                print('No arrival data received. Trying again in 10 seconds.')
        
    except:
        pass
        
    time.sleep(delay);
