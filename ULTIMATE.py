#Created by Sebastian Kleivenes for Fuel Fighter
#NB: execfile('/flash/ULTIMATE.py')
import _thread
from machine import UART
from machine import SD
from utime import ticks_ms as ut
from time import sleep as ts
global sd,CAN_COUNT,OLD_CAN_ID,ID_FORMAT_INFO,brake,stw,bmss,brake,bms1,bms2,bms3,bmst,bmsvc,bmsef,mos,mts,s_try,sp,sp2,reason,temp,enco,dashb,frontls,rearls,py,acc,acc_count,acc_file,error_file,os_file,session,CANID,SERVER_DATA,elcl_1,elcl_2,mcMSG1,mcMSG2
sd = SD()
print('Files on the SD-Card.\n'+str(os.listdir('/sd')))
if "session.txt" in ls('/sd'):
    ses=open('/sd/session.txt','r')
    session=int(ses.read())+1
    ses.close()
    ts(0.1)
    mkdir('/sd/'+str(session))
    ts(0.1)
    ses=open('/sd/session.txt','w+')
    ses.write(str(session))
    ses.close()
else:
    ses=open('/sd/session.txt','w+')
    session=1
    ses.write(str(session))
    ses.close()
    mkdir('/sd/'+str(session))
uart2 = UART(1, baudrate=500000, pins=('P3','P21'))#NB!TXD=P3, RXD=P21#NB!PIN P2 CONFLICT WITH RGB CONTROL
SERVER_DATA={'0':0,#Time (s)
        '1':0,#BMS State (0/1/2/3)
        '2':0,#BMS ERROR FLAG: PreChargeTimeout (True/False)
        '3':0,#BMS ERROR FLAG: LTC_LossOfSignal (True/False)
        '4':0,#BMS ERROR FLAG: OverVoltage (True/False)
        '5':0,#BMS ERROR FLAG: UnderVoltage (True/False)
        '6':0,#BMS ERROR FLAG: OverCurrent (True/False)
        '7':0,#BMS ERROR FLAG: OverTemp (True/False)
        '8':0,#BMS ERROR FLAG: NoDataOnStartup (True/False)
        '9':0,#BMS Battery Current
        '10':0}#BMS Battery Voltage#NB Not in use!
OLD_CAN_ID={'110':'Brake',
            '120':'Electric_Clutch_1',
            '220':'Electric_Clutch_2',
            '230':'Steering_Wheel',
            '250':'Motor_1_Status',
            '251':'Motor_1_MSG',
            '260':'Motor_2_Status',
            '261':'Motor_2_MSG',
            '310':'Dashboard',
            '440':'BMS_Cell_V_1_4',
            '441':'BMS_Cell_V_5_8',
            '442':'BMS_Cell_V_9_12',
            '443':'BMS_Cell_Temp',
            '444':'BMS_Volt_Current',
            '448':'BMS_State',
            '449':'BMS_Error_Flags',
            '470':'Front_Lights_Status',
            '480':'Rear_Lights_Status',
            'acc':'Accelerometer',
            'error':'ERROR',
            'os':'RUN_INFO'}
ID_FORMAT_INFO={'110':'Time, Brake',
            '120':'Time, Motor Speed (RPM), Clutch Status (0/1/2)',
            '220':'Time, Motor Speed (RPM), Clutch Status (0/1/2)',
            '230':'Time, GearOne, GearTwo, GearType',
            '250':'Time, Motor1StatusByte, Current (A), Bat-volt (V), Used energy (kJ), Speed (km/h), Motor Temp',
            '251':'Time, Gear Required (0/1/2)',
            '260':'Time, Motor2StatusByte, Current (A), Bat-volt (V), Used energy (kJ), Speed (km/h), Motor Temp',
            '261':'Time, Gear Required (0/1/2)',
            '310':'Time, Lights, Hazards, Lap, LightLevel, WinWiperLevel, WinWiperState',
            '440':'Time, Cell_V1, V2, V3, V4',
            '441':'Time, Cell_V5, V6, V7, V8',
            '442':'Time, Cell_V9, V10, V11, V12',
            '443':'Time, Cell_Temp_1, 2, 3, 4',
            '444':'Time, BatCurrent, BatVoltage',
            '448':'Time, State',
            '449':'Time, PreChargeTimeout, LTC_LossOfSignal, OverVoltage, UnderVoltage, OverCurrent, OverTemp, NoDataOnStartup',
            '470':'Time, HeadlightLvl, HeadlightState, Blinker(Left/Right)=T/F, Hazards',
            '480':'Time, RearLightLvl, RearLightState, Blinker(Left/Right)=T/F, Hazards, Brakelights',
            'acc':'Time, Pitch, Roll',
            'error':'Time, Input, Error Reason',
            'os':'# of None, Time of Start, Time of End, Delta Time, Setting, Failed, Successes'}
CAN_COUNT={'110':-1,
            '120':-1,
            '220':-1,
            '230':-1,
            '250':-1,
            '251':-1,
            '260':-1,
            '261':-1,
            '310':-1,
            '440':-1,
            '441':-1,
            '442':-1,
            '443':-1,
            '444':-1,
            '448':-1,
            '449':-1,
            '470':-1,
            '480':-1,
            'acc':-1,
            'error':-1,
            'os':-1}
LED(LED_green_soft)
if True:
    g=None
    bmss=None
    brake=None
    bms1=None
    bms2=None
    bms3=None
    stw =None
    bmst =None
    bmsvc=None
    bmsef=None
    mos=None
    mts=None
    mcMSG1=None
    mcMSG2=None
    elcl_1=None
    elcl_2=None
    s_try=True
    l_count=0
    enco=None
    dashb=None
    frontls=None
    os_file=None
    rearls=None
    sp=', '#Seperator between values ', ' for csv
    sp2='_'#Seperator between filename and number
    success=0
    failed=0
    C=0
    none_count=0
    acc_count=0
    acc_file=None
    error_file=None
    server_count=None
setting=100000#How many runs to do 1h~=50 000 but this varied wildly
USE_SERVER=False
def send_server():
    global sd
    from network import WLAN
    from mqtt import MQTTClient
    import machine
    import time
    def sub_cb(topic, msg):
       print(msg)

    wlan = WLAN(mode=WLAN.STA)
    wlan.connect("Android", auth=(WLAN.WPA2, "123456789a"), timeout=5000)

    while not wlan.isconnected():
        machine.idle()
    print("Connected to Wifi\n")

    client = MQTTClient("FiPy", "129.241.91.125",user="username", password="ff", port=1883)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic="Fuelfighter")
    last=None
    packetTemp=None
    copy_counter=0
    while True:
        stime=(ut()+500)//1000
        if "server.txt" in ls('/sd') and stime!=last:
            last=stime
            file=open('/sd/server.txt','r')
            packet=file.read()
            file.close()
            if packet!=packetTemp:
                client.publish(topic="Fuelfighter", msg=packet)
                client.check_msg()
def time_c(a):
    if int(a)>999:
        a=a[0:len(a)-3]+'.'+a[len(a)-3:len(a)]
    return a
def define_data(g):
    Data={}
    for i in range(1,(int(g[4:5]))+1):
        Data[i-1]=g[2*i+4:2*i+6]
    return Data
def calculateVelocity(RPM):
    TIRE_DIAMETER = 0.55
    RPM_TO_METER_P_SECOND = (TIRE_DIAMETER * 3.14159) / 60
    velocity = RPM*RPM_TO_METER_P_SECOND
    if velocity > 50.0:
        velocity = 0
    return velocity
def calculateKmh(velocity):
	return velocity*3.6
def store(r_v):
    global sd,CAN_COUNT,OLD_CAN_ID,ID_FORMAT_INFO,brake,stw,bmss,brake,bms1,bms2,bms3,bmst,bmsvc,bmsef,mos,mts,s_try,sp,sp2,reason,temp,enco,dashb,frontls,rearls,py,acc,acc_count,acc_file,error_file,os_file,session,elcl_1,elcl_2,mcMSG1,mcMSG2
    CAN_COUNT[CANID]+=1
    filename=OLD_CAN_ID[CANID]
    linje=CAN_COUNT[CANID]//50
    rest=CAN_COUNT[CANID]-(linje*50)
    name=str(filename+sp2+str(linje)+'.csv')
    place=r'/sd/'+str(session)
    if rest==0:
        if linje>0:
            temp.close()
        temp=open(place+r'/'+name, 'a+')
        temp.write(str(ID_FORMAT_INFO[CANID])+'\n')
    if name in ls(place) and CANID!='os':
        temp.write(time+', '+r_v+'\n')
    if name in ls(place) and CANID=='os':
        temp.write(r_v+'\n')
def process(Data):
    global sd,CAN_COUNT,OLD_CAN_ID,ID_FORMAT_INFO,brake,stw,bmss,brake,bms1,bms2,bms3,bmst,bmsvc,bmsef,mos,mts,s_try,sp,sp2,reason,temp,enco,dashb,frontls,rearls,py,acc,acc_count,acc_file,error_file,os_file,session,SERVER_DATA,elcl_1,elcl_2,mcMSG1,mcMSG2
    ID=OLD_CAN_ID[CANID]
    if ID == 'Brake':#Brake Engaged
        r_v=str(int(Data[0],16))
        temp=brake
        store(r_v)
        brake=temp
    elif ID == 'Electric_Clutch_1' or ID == 'Electric_Clutch_2':#Motor speed (RPM) : Clutch Status (0/1/2)
        MotorRPM = int(Data[1] + Data[0], 16)
        ClutchStatus = int(Data[2], 16)
        r_v = str(MotorRPM)+sp+str(ClutchStatus)
        if ID == 'Electric_Clutch_1':
            temp=elcl_1
            store(r_v)
            elcl_1=temp
        if ID == 'Electric_Clutch_2':
            temp=elcl_2
            store(r_v)
            elcl_2=temp
    elif ID == 'Steering_Wheel':#GearOne : GearTwo : GearType
        ThrottleRight = int(Data[3], 16)
        ThrottleLeft = int(Data[2], 16)
        buttons = int(Data[1],16)
        if buttons & 0b1:
            GearOne = True
        else:
            GearOne = False
        if buttons & 0b10:
            GearTwo = True
        else:
            GearTwo = False
        if buttons & 0b100:
            GearType = "Auto"
        else:
            GearType = "Manual"
        r_v=str(GearOne)+sp+str(GearTwo)+sp+str(GearType)
        temp=stw
        store(r_v)
        stw=temp
    elif ID == 'Dashboard':#Lights : Hazards : Lap : LightLevel : WinWiperLevel : WinWiperState
        buttons = int(Data[0],16)
        if buttons & 0b1:
            Lights = True
        else:
            Lights = False
        if buttons & 0b10:
            Hazards = True
        else:
            Hazards = False
        if buttons & 0b100:
            Lap = True
        else:
            Lap = False
        Light_Level = int(Data[1],16)
        WindowWiper_Level = int(Data[2],15)

        if WindowWiper_Level > 5:
            WindowWiper_State = True
        else:
            WindowWiper_State = False
        r_v=str(Lights)+sp+str(Hazards)+sp+str(Lap)+str(Light_Level)+sp+str(WindowWiper_Level)+sp+str(WindowWiper_State)
        temp=dashb
        store(r_v)
        dashb=temp
    elif ID == 'BMS_Cell_V_1_4' or ID == 'BMS_Cell_V_5_8' or ID == 'BMS_Cell_V_9_12':#Cell_V1 : V2 : V3 : V4
        r_v=str(int(Data[1] + Data[0], 16)/10000)+sp+str(int(Data[3] + Data[2], 16)/10000)+sp+str(int(Data[5] + Data[4], 16)/10000)+sp+str(int(Data[7] + Data[6], 16)/10000)
        if ID == 'BMS_Cell_V_1_4':
            temp=bms1
            store(r_v)
            bms1=temp
        if ID == 'BMS_Cell_V_5_8':
            temp=bms2
            store(r_v)
            bms2=temp
        if ID == 'BMS_Cell_V_9_12':
            temp=bms3
            store(r_v)
            bms3=temp
    elif ID == 'BMS_Cell_Temp':#Cell_Temp_1 : 2 : 3 : 4
        r_v=str(int(Data[1] + Data[0], 16))+sp+str(int(Data[3] + Data[2], 16))+sp+str(int(Data[5] + Data[4], 16))+sp+str(int(Data[7] + Data[6], 16))
        temp=bmst
        store(r_v)
        bmst=temp
    elif ID == 'BMS_Volt_Current':#BatCurrent : BatVoltage
        r_v=str(int(Data[1] + Data[0], 16))+sp+str(int(Data[3] + Data[2], 16)/1000)
        SERVER_DATA['9']=str(int(Data[1] + Data[0], 16))
        SERVER_DATA['10']=str(int(Data[3] + Data[2], 16))
        temp=bmsvc
        store(r_v)
        bmsvc=temp
    elif ID == 'BMS_State':#State
        State = int(Data[0], 16)
        SERVER_DATA['1']=str(State)
        if State == 0:
            r_v = 'Idle'
        elif State == 1:
            r_v = 'PreCharge'
        elif State == 2:
            r_v = 'Battery Active'
        elif State == 3:
            r_v = 'Error'
        else:
            r_v = 'StateStatus Error'
        temp=bmss
        store(r_v)
        bmss=temp
    elif ID == 'BMS_Error_Flags':#PreChargeTimeout : LTC_LossOfSignal : OverVoltage : UnderVoltage : OverCurrent : OverTemp : NoDataOnStartup
        errorFlag = int(Data[0], 16)
        if errorFlag & 0b1:
            Error_PreChargeTimeout = True
            SERVER_DATA['2']='1'
        else:
            Error_PreChargeTimeout = False
            SERVER_DATA['2']='0'
        if errorFlag & 0b10:
            Error_LTC_LossOfSignal = True
            SERVER_DATA['3']='1'
        else:
            Error_LTC_LossOfSignal = False
            SERVER_DATA['3']='0'
        if errorFlag & 0b100:
            Error_OverVoltage = True
            SERVER_DATA['4']='1'
        else:
            Error_OverVoltage = False
            SERVER_DATA['4']='0'
        if errorFlag & 0b1000:
            Error_UnderVoltage = True
            SERVER_DATA['5']='1'
        else:
            Error_UnderVoltage = False
            SERVER_DATA['5']='0'
        if errorFlag & 0b10000:
            Error_OverCurrent = True
            SERVER_DATA['6']='1'
        else:
            Error_OverCurrent = False
            SERVER_DATA['6']='0'
        if errorFlag & 0b100000:
            Error_OverTemp = True
            SERVER_DATA['7']='1'
        else:
            Error_OverTemp = False
            SERVER_DATA['7']='0'
        if errorFlag & 0b1000000:
            Error_NoDataOnStartup = True
            SERVER_DATA['8']='1'
        else:
            Error_NoDataOnStartup = False
            SERVER_DATA['8']='0'
        r_v=str(Error_PreChargeTimeout)+sp+str(Error_LTC_LossOfSignal)+sp+str(Error_OverVoltage)+sp+str(Error_UnderVoltage)+sp+str(Error_OverCurrent)+sp+str(Error_OverTemp)+sp+str(Error_NoDataOnStartup)
        temp=bmsef
        store(r_v)
        bmsef=temp
    elif ID == 'Motor_1_Status' or ID == 'Motor_2_Status':#MotorStatusByte OFF : ACC : BRAKE : IDLE : ERROR : Current (A) : Bat-volt (V) : Used energy (kJ) : Speed (km/h) : Motor Temp
        MotorStatusByte = int(Data[0],16)
        if MotorStatusByte == 0:
            MSB = 'OFF'
        elif MotorStatusByte == 1:
            MSB = 'ACC'
        elif MotorStatusByte == 2:
            MSB = 'BRAKE'
        elif MotorStatusByte == 3:
            MSB = 'IDLE'
        elif MotorStatusByte == 4:
            MSB = 'ERROR'
        elif MotorStatusByte == 5:
            MSB = 'ENGAGE'
        M_Current = (int(Data[1], 16))
        try:
            if M_Current>127:
                M_Current-=256
            M_Current=M_Current/10
        except:
            M_Current=M_Current/10
        M_Volt = (int(Data[3] + Data[2], 16))/10
        M_Energy = (int(Data[5] + Data[4], 16))/100
        M_Speed = (int(Data[6], 16))/5
        M_Temp = int(Data[7], 16)
        r_v=str(MSB)+sp+str(M_Current)+sp+str(M_Volt)+sp+str(M_Energy)+sp+str(M_Speed)+sp+str(M_Temp)
        if ID == 'Motor_1_Status':
            temp=mos
            store(r_v)
            mos=temp
        if ID == 'Motor_2_Status':
            temp=mts
            store(r_v)
            mts=temp
    elif ID == 'Motor_1_MSG' or ID == 'Motor_2_MSG':#Gear Required (0/1/2)
        GearRequired = int(Data[0],16)
        r_v=str(GearRequired)
        if ID == 'Motor_1_MSG':
            temp=mcMSG1
            store(r_v)
            mcMSG1=temp
        if ID == 'Motor_2_MSG':
            temp=mcMSG2
            store(r_v)
            mcMSG2=temp
    elif ID == 'Front_Lights_Status' or ID == 'Rear_Lights_Status':#HeadlightLvl : HeadlightState : Blinker(Left/Right)=T/F : Hazards // #RearLightLvl : RearLightState : Blinker(Left/Right)=T/F : Hazards:Brakelights
        Light_level = int(Data[1],16)
        states = int(Data[0],16)
        if states & 0b1:
            Lights = True
        else:
            Lights = False
        if states & 0b10:
            BlinkerLeft = True
            blinker = 'L-True'
        else:
            BlinkerRight = False
            blinker = 'R-False'
        if states & 0b100:
            Hazards = True
        else:
            Hazards = False
        r_v=str(Light_level)+sp+str(Lights)+sp+str(blinker)+sp+str(Hazards)
        if ID == 'Front_Lights_Status':
            temp=frontls
            store(r_v)
            frontls=temp
        if ID == 'Rear_Lights_Status':
            if states & 0b1000:
                Brakelights = True
            else:
                Brakelights = False
            r_v+=sp+str(Brakelights)
            temp=rearls
            store(r_v)
            rearls=temp
    else:
        pass
def qualityControl(g):#Checks Integrity of data
    global sd,CAN_COUNT,OLD_CAN_ID,ID_FORMAT_INFO,brake,stw,bmss,brake,bms1,bms2,bms3,bmst,bmsvc,bmsef,mos,mts,s_try,sp,sp2,reason,temp,enco,dashb,frontls,rearls,py,acc,acc_count,acc_file,error_file,os_file,session,CANID,elcl_1,elcl_2,mcMSG1,mcMSG2
    try:
        g=g.decode('ascii')
        try:
            g=str(g)
            try:
                g=g[1:(len(g)-2)]
                try:
                    CANID=g[0:3]
                    if len(g)==(6+(int(g[4:5]))*2):
                        try:
                            Data=define_data(g)
                            return Data
                        except:
                            reason='01'
                            s_try=False
                    else:
                        s_try=False
                        reason='02'
                        return False
                except:
                    reason='03'
                    s_try=False
            except:
                reason='04'
                s_try=False
        except:
            reason='05'
            s_try=False
    except:
        reason='06'
        s_try=False
    return False
int_time=time_c(str(ut()))
if USE_SERVER==True:
    _thread.start_new_thread(send_server,())
while C<setting:
    time=ut()
    rtime=time//1000
    time=time_c(str(time))
    if server_count!=rtime and USE_SERVER==True:
        server_count=rtime
        SERVER_DATA['0']=rtime
        to_server=open('/sd/server.txt','w+')
        for i in range(1,11):
            if i==1:
                packet=str(SERVER_DATA['0'])
            packet+=sp+str(SERVER_DATA[str(i)])
        packet=packet.replace(' ', '')
        to_server.write(packet)
        to_server.close()
    g=uart2.readline()
    #g=rb'[448:1:01]\n'#For checking syntax without CAN connected
    s_try=True
    reason='00'
    C+=1
    if True:#For feedback, and feedback logging only, not critical
        if (C//1000)*1000==C:
            print(ls('/sd'))
        if g==None:
            none_count+=1
            LED(LED_pink_soft)
            continue
        if C%100==0 and failed<success:
            l_count+=1
            if l_count%2==0:
                LED(LED_green_soft)
            else:
                LED(LED_yellow_soft)
        if failed>success:
            LED(LED_red_soft)
    if s_try==True:#Where data is processed
        try:
            Data=qualityControl(g)
            if s_try==True and Data!=False:
                try:
                    process(Data)
                    success+=1
                    continue
                except:
                    reason=''
                    s_try=False
        except:
            reason='09'
            s_try=False
    if s_try==False:#When something went wrong in Data processing
        failed+=1
        r_v=str(g)+sp+reason
        CANID='error'
        temp=error_file
        store(r_v)
        error_file=temp
r_v=str(none_count)+sp+str(int_time)+sp+str(time)+sp+str(setting)+sp+str(failed)+sp+str(success)
CANID='os'
temp=os_file
store(r_v)
os_file=temp
if True:#Python only writes to sd when .close() is run, hence to not lose last <500 lines, .close() must be run
    try:
        brake.close()
    except:
        pass
    try:
        bms1.close()
    except:
        pass
    try:
        stw.close()
    except:
        pass
    try:
        bms2.close()
    except:
        pass
    try:
        bmss.close()
    except:
        pass
    try:
        bmst.close()
    except:
        pass
    try:
        bmsvc.close()
    except:
        pass
    try:
        bmsef.close()
    except:
        pass
    try:
        mos.close()
    except:
        pass
    try:
        bms3.close()
    except:
        pass
    try:
        temp.close()
    except:
        pass
    try:
        enco.close()
    except:
        pass
    try:
        dashb.close()
    except:
        pass
    try:
        frontls.close()
    except:
        pass
    try:
        rearls.close()
    except:
        pass
    try:
        mts.close()
    except:
        pass
    try:
        error_file.close()
    except:
        pass
    try:
        os_file.close()
    except:
        pass
print('the following files exist on the SD-Card.\n'+str(os.listdir('/sd')))
LED(LED_off)
for i in range(5):
    LED(LED_red_soft)
    ts(1)
    ts(LED_off)
    ts(1)
