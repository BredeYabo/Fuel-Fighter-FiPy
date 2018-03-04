#Created by Sebastian Kleivenes for Fuel Fighter
#notes
#   uart.read(10)       # read 10 characters, returns a bytes object
#   uart.readall()      # read all available characters
#   uart.readline()     # read a line#NB THIS IS THE ONLY METHOD USED
#   uart.readinto(buf)  # read and store into the given buffer
#   uart.write('abc')   # write the 3 characters
#f = open('/sd/data_collection.txt', 'r')
#f.readall()
#uart.readline()
#f.close()
#NB: PIN 4, 8 & 23 are used by SD card
#NB: PIN 3 & are default pins for UART
#need to use alternative pins for UART, SD card pins CANNOT be changed
#uart.init(baudrate=9600, bits=8, parity=None, stop=1, * , timeout_chars=2, pins=(TXD, RXD, RTS, CTS))
#NB:execfile('/flash/UART_ULTIMATE.py')
#bit=(int(g[7:8]))
from machine import UART
from machine import SD
from utime import ticks_ms as t
from time import sleep as ts
import os
sd = SD()
uart = UART(1, baudrate=500000, pins=('P2','P21'))#NB!TXD=P2, RXD=P21#NB!PIN P2 CONFLICT WITH RGB CONTROL
print("Files on the SD-Card.\n"+str(os.listdir('/sd')))
CAN_ID={'110':'Brake','220':'Encoder','230':'Steering_Wheel','310':'Dashboard','440':'BMS_Cell_V_1-4','441':'BMS_Cell_V_5-8','442':'BMS_Cell_V_9-12','443':'BMS_Cell_Temp','444':'BMS_Volt_Current','448':'BMS_State','449':'BMS_Error_Flags','450':'Motor_1_Status','460':'Motor_2_Status','470':'Front_Lights_Status','480':'Rear_Lights_Status'}
#FAKE_NEWS={'130':'Brake','220':'Encoder','240':'Steering_Wheel','305':'Dashboard','440':'BMS_Cell_V_1-4','441':'BMS_Cell_V_5-8','140':'BMS_Cell_V_9-12','210':'BMS_Cell_Temp','150':'BMS_Volt_Current','331':'BMS_State','215':'BMS_Error_Flags','202':'Motor_1_Status','223':'Motor_2_Status','470':'Front_Lights_Status','480':'Rear_Lights_Status'}
#Initializing values FAKE_NEWS = Simulated fake data
#Example of data g=r"b'[230:6:00\x0000\x0118\x020B\x0364\x043E\x05]\n"
#                       230 6 00    00    18    0B    64    3E
hb(False)
g=""
temp=""
C=0#Should be removed in final
s_try=True
none_count=0
copy_read=0
setting=2000#How many runs to do
def time_c(a):
    if int(a)>999:
        a=a[0:len(a)-3]+"."+a[len(a)-3:len(a)]
    return a
def process(g,time):
    data=""
    for i in range(1,(int(g[7:8]))+1):
        if i==(int(g[7:8])):
            data+=g[6*i+3:6*i+5]+":"+time
        else:
            data+=g[6*i+3:6*i+5]+" "
    return data
def write_sd(filename,data):
    f = open(r"/sd/"+filename+".txt", 'a+')
    f.write(data+"\n")
    f.close()
int_time=time_c(str(t()))
while C<setting:#"while True:" when not testing/when finnished
    g=str(uart.readline())
    time=time_c(str(t()))
    reason="-00"
    C+=1
    s_try=True
    if g!="None" and g!=temp and g!="":
        try:
            if len(g)==(13+(int(g[7:8]))*6) and ((int(g[7:8]))%2)==0:
                data=process(g,time)
                write_sd(CAN_ID[g[3:6]],data)
                temp=g
                s_try=True
            else:
                reason="-01"
                s_try=False
        except:
            reason="-02"
            s_try=False
    if temp==g and g!="None":
        copy_read+=1
    if g=="None":
        none_count+=1
    if s_try==False:
        f = open("/sd/ERRORS.txt", 'a+')
        f.write("{"+g+"}:"+time+":ERROR"+reason+"\n")
        f.close()
if none_count>0 or copy_read>0:
    f = open("/sd/ERRORS.txt", 'a+')
    f.write("# of 'None' = "+str(none_count)+" # of repeat reads from UART = "+str(copy_read)+" : T_start = "+int_time+" : T_end = "+time+"Setting="+str(setting)+"\n")
    f.close()
print("the following files exist on the SD-Card.\n"+str(os.listdir('/sd')))
