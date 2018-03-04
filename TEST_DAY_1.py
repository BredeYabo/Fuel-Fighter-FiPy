#Program specifically made for first test of Car by Sebastian Kleivenes
#execfile('/flash/TEST_DAY_1.py')To run this file
#
#data=g[9:11]+' '+g[15:17]
#if bit==4:
#data+=' '+g[21:23]+' '+g[27:29]
#else if bit==6:
#data+=' '+g[21:23]+' '+g[27:29]+' '+g[33:35]+' '+g[39:41]
#else if bit==8:
#data+=' '+g[21:23]+' '+g[27:29]+' '+g[33:35]+' '+g[39:41]+' '+g[45:47]+' '+g[51:53]
#else if bit==10:
#data+=' '+g[21:23]+' '+g[27:29]+' '+g[33:35]+' '+g[39:41]+' '+g[45:47]+' '+g[51:53]+' '+g[57:59]+' '+g[63:65]
#
from machine import UART
from machine import SD
from utime import ticks_ms as t
from time import sleep as ts
import os
sd = SD()
uart = UART(1, baudrate=4800, pins=('P2','P21'))#TXD=P2, RXD=P21
print("the following files exist on the SD-Card.\n"+str(os.listdir('/sd')))
#REAL ID --> CAN_ID={110:'Brake',220:'Encoder',230:'Steering_Wheel',310:'Dashboard',440:'BMS_Cell_V_1-4',441:'BMS_Cell_V_5-8',442:'BMS_Cell_V_9-12',443:'BMS_Cell_Temp',444:'BMS_Volt_Current',448:'BMS_State',449:'BMS_Error_Flags',450:'Motor_1_Status',460:'Motor_2_Status',470:'Front_Lights_Status',480:'Rear_Lights_Status'}
CAN_ID={'130':'Brake','220':'Encoder','240':'Steering_Wheel','305':'Dashboard','440':'BMS_Cell_V_1-4','441':'BMS_Cell_V_5-8','140':'BMS_Cell_V_9-12','210':'BMS_Cell_Temp','150':'BMS_Volt_Current','331':'BMS_State','215':'BMS_Error_Flags','202':'Motor_1_Status','460':'Motor_2_Status','470':'Front_Lights_Status','480':'Rear_Lights_Status'}
#FAKE CANID^^^^^^^ID values
#Initializing values
hb(False)
g=""
temp=""
error=False
C_FAILURE=False
C_ID_TRY=False
Count=0#Should be removed in final
F_NID=""
s_try=False
none_count=0
int_time=str(t())
while Count<1000:#"while True:" when not testing/when finnished
    g=str(uart.readline())
    time=str(t())
    original=g
    Count+=1
    if original=="None":
        none_count+=1
    try:
        g=g[3:len(g)-4]
        bit=(int(g[4:5]))*2
        if len(g)==(6+bit):
            s_try=True
        else:
            s_try=False
    except:
        s_try=False
        if original!="None":
            f = open("/sd/ERRORS.txt", 'a+')
            if int(time)>999:
                f.write("FTS: {"+original+"} : TIME="+time[0:len(time)-3]+"."+time[len(time)-3:len(time)]+"\n")
            else:
                f.write("FTS: {"+original+"} : TIME="+time+"\n")
            f.close()
    if temp!=g and g!="" and original!="None" and s_try==True:
        try:#Attempts to sort data, recoqnize type/CANID and write to appropriate .txt file, and if any of this goes wrong it'll write the failed to sort data to ERRORS.txt
            file_name=CAN_ID[g[0:3]]
            f_name=r"/sd/"+file_name+".txt"
            f = open(f_name, 'a+')
            if int(time)>999:
                f.write(g[6:(6+bit)]+" : T="+time[0:len(time)-3]+"."+time[len(time)-3:len(time)]+"\n")
            else:
                f.write(g[6:(6+bit)]+" : T="+time+"\n")
            f.close()
            temp=g
        except:
            f = open("/sd/ERRORS.txt", 'a+')
            if int(time)>999:
                f.write("FTS: {"+original+"} : TIME="+time[0:len(time)-3]+"."+time[len(time)-3:len(time)]+"\n")
            else:
                f.write("FTS: {"+original+"} : TIME="+time+"\n")
            f.close()

if none_count>0:
    f = open("/sd/ERRORS.txt", 'a+')
    f.write("Total number of 'None' i.e. 'empty UART readings' = "+str(none_count)+" And time of run completion = "+time[0:len(time)-3]+"."+time[len(time)-3:len(time)]+"  Time Began: "+int_time+"\n")
    f.close()
if C_FAILURE==True:
    from pycom import rgbled as LED
    green=0x007f00
    red=0x7f0000
    yellow=0x7f7f00
    for i in range(0,5):
        LED(0x000000)
        ts(1)
        LED(0x7f0000)
        ts(1)
print("the following files exist on the SD-Card.\n"+str(os.listdir('/sd')))
