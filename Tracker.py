import serial
import os, time
import math

ser = serial.Serial('/dev/serial0', 115200, timeout=1)
ser.reset_input_buffer()

def convert_gps(x,sign,Type):
    if(Type == "lat") :
        d = float(x[0:2])
        m = float(x[2:])
    else :
        d = float(x[0:3])
        m = float(x[3:])
        
    result = d + (m / 60)
    if(sign == "E" or sign == "N") :
        return result
    else :
        return -result

#Calculating distance
def calcDist(lat1,long1,lat2,long2): 
    r = 6371
    dlat = (lat2-lat1)*(math.pi / 180)
    dlon = (long2-long1)*(math.pi / 180)
    a = math.sin(dlat / 2) * math.sin(dlat/2) + math.cos(lat1 * (math.pi / 180)) * math.cos(lat2 * (math.pi / 180)) * (math.sin(dlon/2)**2)
    c = 2* math.atan2(math.sqrt(a), math.sqrt(1-a))
    return r*c   
    
def checkZone(x,y):  #insert x,y coordinates for child 
    #Allowed Zones Coordinates
    rectList = [("Home",[30.06054,31.34541,30.06332,31.34931]),("School",[30.06011,31.34733,30.06038,31.34779]),("Club",[30.05993,31.34569,30.06022,31.3462])]
    dist = []
    minDist = 0
    Box = []
    for i in rectList : # loop for checking in each zone 
        x1 = i[1][0] # x1 for zone (bottom-left)
        y1 = i[1][1] # y1 for zone (bottom-left)
        x2 = i[1][2] # x2 for zone (up-right)
        y2 = i[1][3] # y2 for zone (up-right)
        
        #checking location position GreenZone\RedZone
        if(x1<x<x2 and y1<y<y2):
            Box.append("GreenZone")
            Box.append(i[0])
            return Box
        
        dist1 = calcDist(x, y, x1, y1)
        dist2 = calcDist(x, y, x2, y2)
        dist.append(min(dist1,dist2))
        
    minDist = min(dist)
    nearBy = rectList[dist.index(minDist)][0]
    Box.append("RedZone")
    Box.append(nearBy)
    Box.append(minDist)
    return Box

def GPS_ON():
    while True :
        cmd ="AT+CGPSPWR=1"+"\r\n"
        cmds=cmd.encode("utf-8")
        ser.write(cmds)
        time.sleep(1)
        lines = ser.readlines()

        if len(lines)>1 :
            if(lines[1].strip().decode("utf-8") == "OK"):
                print("GPS is ON")
                break; 
     
                 
def GPS_Read_Location(Phone):
    previousTime = 0
    while True:
        currentTime = time.time()
        send = False
        cmd ="AT+CGPSINF=2"+'\r\n'
        cmds=cmd.encode("utf-8")
        ser.write(cmds)
        time.sleep(1)
        lines = ser.readlines()
        if (len(lines) > 1 and "+CGPSINF" in lines[1].strip().decode("utf-8")) :
            print("GPS is Reading")
            gps = lines[1].decode('utf-8')
            gps = gps.split(",")
            lat = gps[2]
            lat_sign = gps[3]
            lat = convert_gps(lat,lat_sign,"lat")
            lon = gps[4]
            lon_sign = gps[5]
            lon = convert_gps(lon,lon_sign,"lon")
            print("Current Location: "+str(lat)+","+str(lon))
            result = checkZone(lat,lon)
            
            url = "http://www.bing.com/maps?q=" + str(lat) + ',' + str(lon)
            
            if result[0] == "GreenZone" :
                msg = "Child in GreenZone ("+result[1]+") \nlat: "+str(lat)+"\nlon: "+str(lon)+"\nLocation: " +url
            else :
                msg = "Child in RedZone \nlat: "+str(lat)+"\nlon: "+str(lon)+"\nNearby:"+result[1]+"("+str(result[2])+" KM)\nLocation: "+url
                send = True
            
            if ( currentTime - previousTime > 60):
                send = True
                previousTime = currentTime
                
            if send :
                Send_Message(msg,Phone)
                break;
            
def Send_Message(MSG,Phone):
    while True :
        cmd="AT+CMGF=1"+"\r"
        cmds=cmd.encode("utf-8")
        ser.write(cmds)
        time.sleep(1)
        lines = ser.readlines()
             
        if (len(lines)>1):
            if(lines[1].strip().decode("utf-8") == "OK"):
                print("Ready To Send MSG")
                cmd='AT+CMGS="'+Phone+'"'+'\r\n'
                cmds=cmd.encode("utf-8")
                ser.write(cmds)
                time.sleep(1)
                
                #Your MSG
                ser.write(MSG.encode("utf-8"))
                time.sleep(1)
                                
                #Cntl+Z
                ser.write(chr(26).encode())
                time.sleep(1)
                
                print("Sent MSG : "+MSG)
                break;
            
Phone = "Your Phone Number"
GPS_ON()
time.sleep(2)
GPS_Read_Location(Phone)

