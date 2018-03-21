#Created by Sebastian Kleivenes for Fuel Fighter
#NB: execfile('/flash/UART_2.py')
#NB! WARNING Accelerometer NOT tested yet with UART, and not included in this version
#NB! AWS yet to be implemented to this file
from machine import UART
from machine import SD
from utime import ticks_ms as ut
from time import sleep as ts
global sd,CAN_COUNT,OLD_CAN_ID,ID_FORMAT_INFO,brake,stw,bmss,brake,bms1,bms2,bms3,bmst,bmsvc,bmsef,mos,mts,s_try,sp,sp2,reason,temp,enco,dashb,frontls,rearls,py,acc,acc_count,acc_file,error_file,os_file,session,CANID
sd = SD()
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
print('Files on the SD-Card.\n'+str(os.listdir('/sd')))
OLD_CAN_ID={'110':'Brake',
            '220':'Encoder',
            '230':'Steering_Wheel',
            '310':'Dashboard',
            '440':'BMS_Cell_V_1_4',
            '441':'BMS_Cell_V_5_8',
            '442':'BMS_Cell_V_9_12',
            '443':'BMS_Cell_Temp',
            '444':'BMS_Volt_Current',
            '448':'BMS_State',
            '449':'BMS_Error_Flags',
            '450':'Motor_1_Status',
            '460':'Motor_2_Status',
            '470':'Front_Lights_Status',
            '480':'Rear_Lights_Status',
            'acc':'Accelerometer',
            'error':'ERROR',
            'os':'RUN_INFO'}
ID_FORMAT_INFO={'110':'Time, Brake',
            '220':'Time, Motor1RPM, Motor2RPM, CarRPM, Velocity',
            '230':'Time, ThrottleRight, ThrottleLeft, JoyX, JoyY, Deadmanswitch, JoyButton, Horn, CCButton, BlinkerL, BlinkerR',
            '310':'Time, Lights, Hazards, Lap, LightLevel, WinWiperLevel, WinWiperState',
            '440':'Time, Cell_V1, V2, V3, V4',
            '441':'Time, Cell_V5, V6, V7, V8',
            '442':'Time, Cell_V9, V10, V11, V12',
            '443':'Time, Cell_Temp_1, 2, 3, 4',
            '444':'Time, BatCurrent, BatVoltage',
            '448':'Time, State',
            '449':'Time, PreChargeTimeout, LTC_LossOfSignal, OverVoltage, UnderVoltage, OverCurrent, OverTemp, NoDataOnStartup',
            '450':'Time, Motor1Status, Throttle, Current, PWM',
            '460':'Time, Motor2Status, Throttle, Current, PWM',
            '470':'Time, HeadlightLvl, HeadlightState, Blinker(Left/Right)=T/F, Hazards',
            '480':'Time, RearLightLvl, RearLightState, Blinker(Left/Right)=T/F, Hazards, Brakelights',
            'acc':'Time, Pitch, Roll',
            'error':'Time, Input, Error Reason',
            'os':'# of None, Time of Start, Time of End, Delta Time, Setting, Failed, Successes'}
CAN_COUNT={'110':-1,
            '220':-1,
            '230':-1,
            '310':-1,
            '440':-1,
            '441':-1,
            '442':-1,
            '443':-1,
            '444':-1,
            '448':-1,
            '449':-1,
            '450':-1,
            '460':-1,
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
setting=750#How many runs to do 1h~=50 000 but this varied wildly
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
    global sd,CAN_COUNT,OLD_CAN_ID,ID_FORMAT_INFO,brake,stw,bmss,brake,bms1,bms2,bms3,bmst,bmsvc,bmsef,mos,mts,s_try,sp,sp2,reason,temp,enco,dashb,frontls,rearls,py,acc,acc_count,acc_file,error_file,os_file,session
    CAN_COUNT[CANID]+=1
    filename=OLD_CAN_ID[CANID]
    linje=CAN_COUNT[CANID]//500
    rest=CAN_COUNT[CANID]-(linje*500)
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
    global sd,CAN_COUNT,OLD_CAN_ID,ID_FORMAT_INFO,brake,stw,bmss,brake,bms1,bms2,bms3,bmst,bmsvc,bmsef,mos,mts,s_try,sp,sp2,reason,temp,enco,dashb,frontls,rearls,py,acc,acc_count,acc_file,error_file,os_file,session
    ID=OLD_CAN_ID[CANID]
    if ID == 'Brake':#Brake Engaged
        r_v=str(int(Data[0],16))
        temp=brake
        store(r_v)
        brake=temp
    elif ID == 'Encoder':#Motor1RPM : Motor2RPM : CarRPM : Velocity
        Velocity = calculateVelocity(int(Data[5] + Data[4], 16))
        r_v = str(int(Data[1] + Data[0], 16))+':'+str(int(Data[3] + Data[2], 16))+':'+str(int(Data[5] + Data[4], 16))+':'+str(Velocity)
        temp=enco
        store(r_v)
        enco=temp
    elif ID == 'Steering_Wheel':#ThrottleRight : ThrottleLeft : JoyX : JoyY : Deadmanswitch : JoyButton : Horn : CCButton : BlinkerL : BlinkerR
        ThrottleRight = int(Data[3], 16)
        ThrottleLeft = int(Data[2], 16)
        JoyX = int(Data[4],16)
        JoyY = int(Data[5],16)
        if ThrottleRight >= 50:
            Deadmanswitch = True
        else:
            Deadmanswitch = False
        buttons = int(Data[1],16)
        if buttons & 0b1:
            JoyButton = True
        else:
            JoyButton = False
        if buttons & 0b10:
            Horn = True
        else:
            Horn = False
        if buttons & 0b100:
            CCButton = True
        else:
            CCButton = False
        if buttons & 0b1000:
            print('BlinkerLeft')
            BlinkerLeft = True
        else:
            BlinkerLeft = False
        if buttons & 0b10000:
            BlinkerRight = True
            print('BlinkerRight')
        else:
            BlinkerRight = False
        r_v=str(ThrottleRight)+sp+str(ThrottleLeft)+sp+str(JoyX)+sp+str(JoyY)+sp+str(Deadmanswitch)+sp+str(JoyButton)+sp+str(Horn)+sp+str(CCButton)+sp+str(BlinkerRight)+sp+str(BlinkerLeft)
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

        if WindowWiper_Level >= 6:
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
        temp=bmsvc
        store(r_v)
        bmsvc=temp
    elif ID == 'BMS_State':#State
        State = int(Data[0], 16)
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
        else:
            Error_PreChargeTimeout = False
        if errorFlag & 0b10:
            Error_LTC_LossOfSignal = True
        else:
            Error_LTC_LossOfSignal = False
        if errorFlag & 0b100:
            Error_OverVoltage = True
        else:
            Error_OverVoltage = False
        if errorFlag & 0b1000:
            Error_UnderVoltage = True
        else:
            Error_UnderVoltage = False
        if errorFlag & 0b10000:
            Error_OverCurrent = True
        else:
            Error_OverCurrent = False
        if errorFlag & 0b100000:
            Error_OverTemp = True
        else:
            Error_OverTemp = False
        if errorFlag & 0b1000000:
            Error_NoDataOnStartup = True
        else:
            Error_NoDataOnStartup = False
        r_v=str(Error_PreChargeTimeout)+sp+str(Error_LTC_LossOfSignal)+sp+str(Error_OverVoltage)+sp+str(Error_UnderVoltage)+sp+str(Error_OverCurrent)+sp+str(Error_OverTemp)+sp+str(Error_NoDataOnStartup)
        temp=bmsef
        store(r_v)
        bmsef=temp
    elif ID == 'Motor_1_Status' or ID == 'Motor_2_Status':#Motor1Status : Throttle : Current : PWM#Motor2Status : Throttle : Current : PWM
        status = int(Data[0],16)
        Throttle = int(Data[1], 16)
        Current = int(Data[2] + Data[3], 16)
        PWM = int(Data[4] + Data[5], 16)
        if status == 0:
            status_r = 'Idle'
        elif status == 1:
            status_r = 'Running'
        elif status == 2:
            status_r = 'Overload'
        else:
            status_r = 'Error obtaining status'
        r_v=str(status_r)+sp+str(Throttle)+sp+str(Current)+sp+str(PWM)
        if ID == 'Motor_1_Status':
            temp=mos
            store(r_v)
            mos=temp
        if ID == 'Motor_2_Status':
            temp=mts
            store(r_v)
            mts=temp
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
    global sd,CAN_COUNT,OLD_CAN_ID,ID_FORMAT_INFO,brake,stw,bmss,brake,bms1,bms2,bms3,bmst,bmsvc,bmsef,mos,mts,s_try,sp,sp2,reason,temp,enco,dashb,frontls,rearls,py,acc,acc_count,acc_file,error_file,os_file,session,CANID
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
while C<setting:
    time=ut()
    time=time_c(str(time))
    #g=uart2.readline()
    g=b'[448:1:01]\n'
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
            if s_try==True & Data!=False:
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
while True:
    LED(LED_red_soft)
    ts(1)
    ts(LED_off)
    ts(1)
