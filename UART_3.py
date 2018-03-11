#Created by Sebastian Kleivenes for Fuel Fighter
#NB:execfile('/flash/UART_3.py')
from machine import UART
from machine import SD
from utime import ticks_ms as ut
from time import sleep as ts
sd = SD()
uart = UART(1, baudrate=500000, pins=('P3','P21'))#NB!TXD=P3, RXD=P21
print("Files on the SD-Card.\n"+str(os.listdir('/sd')))
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
            '480':'Rear_Lights_Status'}
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
            '480':'Time, RearLightLvl, RearLightState, Blinker(Left/Right)=T/F, Hazards, Brakelights'}
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
            '480':-1}
#NEW_CAN_ID={'110':'Dash_Brake','130':'Steering_RegBrake_Throttle','250':'Speed','440':'BMS_Cell_V_1-4','441':'BMS_Cell_V_5-8','442':'BMS_Cell_V_9-12','443':'BMS_Cell_Temp','444':'BMS_Volt_Current','448':'BMS_State','449':'BMS_Error_Flags','450':'Motor_1_Status','460':'Motor_2_Status','470':'Front_Lights_Status','480':'Rear_Lights_Status'}
#Example of data g=r"b'[230:6:00\x0000\x0118\x020B\x0364\x043E\x05]\n"
#                       230 6 00    00    18    0B    64    3E
hb(False)
g=""
success=0
failed=0
temp="bb"
C=0#Should be removed in final
s_try=True
none_count=0
copy_read=0
setting=500#How many runs to do
def time_c(a):
    if int(a)>999:
        a=a[0:len(a)-3]+"."+a[len(a)-3:len(a)]
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
int_time=time_c(str(ut()))
while C<setting:#"while True:" when not testing/when finnished
    reason="-00"
    C+=1
    g=uart.readline()
    try:
        time=time_c(str(ut()))
    except:
        reason="-01"
        s_try=False
    if g==None:
        none_count+=1
        continue
    if g==temp and g!=None:
        copy_read+=1
        continue
    try:
        g=g.decode('ascii')
        try:
            g=str(g)
            try:
                g=g[1:(len(g)-2)]
                try:
                    CANID=g[0:3]
                    try:
                        filename=OLD_CAN_ID[CANID]
                        if len(g)==(6+(int(g[4:5]))*2):
                            s_try=True
                        else:
                            s_try=False
                            reason="-15"
                    except:
                        reason="-05"
                        s_try=False
                except:
                    reason="-06"
                    s_try=False
            except:
                reason="-07"
                s_try=False
        except:
            reason="-08"
            s_try=False
    except:
        reason="-09"
        s_try=False
    if (C//1000)*1000==C:
        print(ls('/sd'))
    if g!="None" and g!=temp and g!="" and s_try==True:
        try:
            data=define_data(g)
            try:
                Data=data
                ID=filename
                sp = ", "
                r_v="NADA"
                sp2="_"
                if ID == 'Brake':#Brake Engaged
                    r_v=str(int(Data[0],16))
                    CAN_COUNT[CANID]+=1
                    linje=CAN_COUNT[CANID]//500
                    rest=CAN_COUNT[CANID]-(linje*500)
                    if rest==0:
                        brake=open("/sd/"+filename+sp2+str(linje)+".csv", "a+")
                        brake.write(str(ID_FORMAT_INFO[CANID])+"\n")
                    if str(filename+sp2+str(linje)+".csv") in ls("/sd"):
                        brake.write(time+", "+r_v+"\n")
                    if rest==499:
                        brake.close()
                elif ID == 'Encoder':#Motor1RPM : Motor2RPM : CarRPM : Velocity
                    Velocity = calculateVelocity(int(Data[5] + Data[4], 16))
                    r_v = str(int(Data[1] + Data[0], 16))+":"+str(int(Data[3] + Data[2], 16))+":"+str(int(Data[5] + Data[4], 16))+":"+str(Velocity)
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
                        print("BlinkerLeft")
                        BlinkerLeft = True
                    else:
                        BlinkerLeft = False
                    if buttons & 0b10000:
                        BlinkerRight = True
                        print("BlinkerRight")
                    else:
                        BlinkerRight = False
                    r_v=str(ThrottleRight)+sp+str(ThrottleLeft)+sp+str(JoyX)+sp+str(JoyY)+sp+str(Deadmanswitch)+sp+str(JoyButton)+sp+str(Horn)+sp+str(CCButton)+sp+str(BlinkerRight)+sp+str(BlinkerLeft)
                    CAN_COUNT[CANID]+=1
                    linje=CAN_COUNT[CANID]//500
                    rest=CAN_COUNT[CANID]-(linje*500)
                    if rest==0:
                        stw=open("/sd/"+filename+sp2+str(linje)+".csv", "a+")
                        stw.write(str(ID_FORMAT_INFO[CANID])+"\n")
                    if str(filename+sp2+str(linje)+".csv") in ls("/sd"):
                        stw.write(time+", "+r_v+"\n")
                    if rest==499:
                        stw.close()
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
                elif ID == 'BMS_Cell_V_1_4':#Cell_V1 : V2 : V3 : V4
                    r_v=str(int(Data[1] + Data[0], 16)/10000)+sp+str(int(Data[3] + Data[2], 16)/10000)+sp+str(int(Data[5] + Data[4], 16)/10000)+sp+str(int(Data[7] + Data[6], 16)/10000)
                    CAN_COUNT[CANID]+=1
                    linje=CAN_COUNT[CANID]//500
                    rest=CAN_COUNT[CANID]-(linje*500)
                    if rest==0:
                        bms1=open("/sd/"+filename+sp2+str(linje)+".csv", "a+")
                        bms1.write(str(ID_FORMAT_INFO[CANID])+"\n")
                    if str(filename+sp2+str(linje)+".csv") in ls("/sd"):
                        bms1.write(time+", "+r_v+"\n")
                    if rest==499:
                        bms1.close()
                elif ID == 'BMS_Cell_V_5_8':#Cell_V5 : V6 : V7 : V8
                    r_v=str(int(Data[1] + Data[0], 16)/10000)+sp+str(int(Data[3] + Data[2], 16)/10000)+sp+str(int(Data[5] + Data[4], 16)/10000)+sp+str(int(Data[7] + Data[6], 16)/10000)
                    CAN_COUNT[CANID]+=1
                    linje=CAN_COUNT[CANID]//500
                    rest=CAN_COUNT[CANID]-(linje*500)
                    if rest==0:
                        bms2=open("/sd/"+filename+sp2+str(linje)+".csv", "a+")
                        bms2.write(str(ID_FORMAT_INFO[CANID])+"\n")
                    if str(filename+sp2+str(linje)+".csv") in ls("/sd"):
                        bms2.write(time+", "+r_v+"\n")
                    if rest==499:
                        bms2.close()
                elif ID == 'BMS_Cell_V_9_12':#Cell_V9 : V10 : V11 : V12
                    r_v=str(int(Data[1] + Data[0], 16)/10000)+sp+str(int(Data[3] + Data[2], 16)/10000)+sp+str(int(Data[5] + Data[4], 16)/10000)+sp+str(int(Data[7] + Data[6], 16)/10000)
                    CAN_COUNT[CANID]+=1
                    linje=CAN_COUNT[CANID]//500
                    rest=CAN_COUNT[CANID]-(linje*500)
                    if rest==0:
                        bms3=open("/sd/"+filename+sp2+str(linje)+".csv", "a+")
                        bms3.write(str(ID_FORMAT_INFO[CANID])+"\n")
                    if str(filename+sp2+str(linje)+".csv") in ls("/sd"):
                        bms3.write(time+", "+r_v+"\n")
                    if rest==499:
                        bms3.close()
                elif ID == 'BMS_Cell_Temp':#Cell_Temp_1 : 2 : 3 : 4
                    r_v=str(int(Data[1] + Data[0], 16))+sp+str(int(Data[3] + Data[2], 16))+sp+str(int(Data[5] + Data[4], 16))+sp+str(int(Data[7] + Data[6], 16))
                    CAN_COUNT[CANID]+=1
                    linje=CAN_COUNT[CANID]//500
                    rest=CAN_COUNT[CANID]-(linje*500)
                    if rest==0:
                        bmst=open("/sd/"+filename+sp2+str(linje)+".csv", "a+")
                        bmst.write(str(ID_FORMAT_INFO[CANID])+"\n")
                    if str(filename+sp2+str(linje)+".csv") in ls("/sd"):
                        bmst.write(time+", "+r_v+"\n")
                    if rest==499:
                        bmst.close()
                elif ID == 'BMS_Volt_Current':#BatCurrent : BatVoltage
                    r_v=str(int(Data[1] + Data[0], 16))+sp+str(int(Data[3] + Data[2], 16)/1000)
                    CAN_COUNT[CANID]+=1
                    linje=CAN_COUNT[CANID]//500
                    rest=CAN_COUNT[CANID]-(linje*500)
                    if rest==0:
                        bmsvc=open("/sd/"+filename+sp2+str(linje)+".csv", "a+")
                        bmsvc.write(str(ID_FORMAT_INFO[CANID])+"\n")
                    if str(filename+sp2+str(linje)+".csv") in ls("/sd"):
                        bmsvc.write(time+", "+r_v+"\n")
                    if rest==499:
                        bmsvc.close()
                elif ID == 'BMS_State':#State
                    State = int(Data[0], 16)
                    if State == 0:
                        r_v = "Idle"
                    elif State == 1:
                        r_v = "PreCharge"
                    elif State == 2:
                        r_v = "Battery Active"
                    elif State == 3:
                        r_v = "Error"
                    else:
                        r_v = "StateStatus Error"
                    CAN_COUNT[CANID]+=1
                    linje=CAN_COUNT[CANID]//500
                    rest=CAN_COUNT[CANID]-(linje*500)
                    if rest==0:
                        bmss=open("/sd/"+filename+sp2+str(linje)+".csv", "a+")
                        bmss.write(str(ID_FORMAT_INFO[CANID])+"\n")
                    if str(filename+sp2+str(linje)+".csv") in ls("/sd"):
                        bmss.write(time+", "+r_v+"\n")
                    if rest==499:
                        bmss.close()
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
                    CAN_COUNT[CANID]+=1
                    linje=CAN_COUNT[CANID]//500
                    rest=CAN_COUNT[CANID]-(linje*500)
                    if rest==0:
                        bmsef=open("/sd/"+filename+sp2+str(linje)+".csv", "a+")
                        bmsef.write(str(ID_FORMAT_INFO[CANID])+"\n")
                    if str(filename+sp2+str(linje)+".csv") in ls("/sd"):
                        bmsef.write(time+", "+r_v+"\n")
                    if rest==499:
                        bmsef.close()
                elif ID == 'Motor_1_Status':#Motor1Status : Throttle : Current : PWM
                    status = int(Data[0],16)
                    Throttle = int(Data[1], 16)
                    Current = int(Data[2] + Data[3], 16)
                    PWM = int(Data[4] + Data[5], 16)
                    if status == 0:
                        status_r = "Idle"
                    elif status == 1:
                        status_r = "Running"
                    elif status == 2:
                        status_r = "Overload"
                    else:
                        status_r = "Error obtaining status"
                    r_v=str(status_r)+sp+str(Throttle)+sp+str(Current)+sp+str(PWM)
                    CAN_COUNT[CANID]+=1
                    linje=CAN_COUNT[CANID]//500
                    rest=CAN_COUNT[CANID]-(linje*500)
                    if rest==0:
                        mos=open("/sd/"+filename+sp2+str(linje)+".csv", "a+")
                        mos.write(str(ID_FORMAT_INFO[CANID])+"\n")
                    if str(filename+sp2+str(linje)+".csv") in ls("/sd"):
                        mos.write(time+", "+r_v+"\n")
                    if rest==499:
                        mos.close()
                elif ID == 'Motor_2_Status':#Motor2Status : Throttle : Current : PWM
                    status = int(Data[0],16)
                    Throttle = int(Data[1], 16)
                    Current = int(Data[2] + Data[3], 16)
                    PWM = int(Data[4] + Data[5], 16)
                    if status == 0:
                        status_r = "Idle"
                    elif status == 1:
                        status_r = "Running"
                    elif status == 2:
                        status_r = "Overload"
                    else:
                        status_r = "Error obtaining status"
                    r_v=str(status_r)+sp+str(Throttle)+sp+str(Current)+sp+str(PWM)
                    CAN_COUNT[CANID]+=1
                    linje=CAN_COUNT[CANID]//500
                    rest=CAN_COUNT[CANID]-(linje*500)
                    if rest==0:
                        bts=open("/sd/"+filename+sp2+str(linje)+".csv", "a+")
                        bts.write(str(ID_FORMAT_INFO[CANID])+"\n")
                    if str(filename+sp2+str(linje)+".csv") in ls("/sd"):
                        bts.write(time+", "+r_v+"\n")
                    if rest==499:
                        bts.close()
                elif ID == 'Front_Lights_Status':#HeadlightLvl : HeadlightState : Blinker(Left/Right)=T/F : Hazards
                    Headlight_Level = int(Data[1],16)
                    states = int(Data[0],16)
                    if states & 0b1:
                        Headlights = True
                    else:
                        Headlights = False
                    if states & 0b10:
                        BlinkerLeft = True
                        blinker="L-True"
                    else:
                        BlinkerRight	= False
                        blinker="R-False"
                    if states & 0b100:
                        Hazards = True
                    else:
                        Hazards = False
                    r_v=str(Headlight_Level)+sp+str(Headlights)+sp+blinker+sp+str(Hazards)
                elif ID == 'Rear_Lights_Status':#RearLightLvl : RearLightState : Blinker(Left/Right)=T/F : Hazards:Brakelights
                    Rearlight_Level = int(Data[1],16)
                    states = int(Data[0],16)
                    if states & 0b1:
                        RearLights = True
                    else:
                        Rearlights = False
                    if states & 0b10:
                        BlinkerLeft = True
                        blinker = "L-True"
                    else:
                        BlinkerRight = False
                        blinker = "R-False"
                    if states & 0b100:
                        Hazards = True
                    else:
                        Hazards = False
                    if states & 0b1000:
                        Brakelights = True
                    else:
                        Brakelights = False
                    r_v=str(Rearlight_Level)+sp+str(Rearlights)+sp+str(blinker)+sp+str(Hazards)+sp+str(Brakelights)
                else:
                    r_v="NoData"
                    pass
                s_try=True
                temp=g
                success+=1
            except:
                reason='-14'
                s_try=False
        except:
            reason='-15'
            s_try=False
    if s_try==False:
        failed+=1
        f = open("/sd/ERRORS.txt", 'a+')
        f.write("{"+g+"} : "+time+" : ERROR"+reason+"\n")
        f.close()
if none_count>0 or copy_read>0:
    f = open("/sd/RUN_INFO.txt", 'a+')
    f.write("# of 'None' = "+str(none_count)+" # of repeat reads from UART = "+str(copy_read)+" : T_start = "+int_time+" : T_end = "+time+"Setting="+str(setting)+"Failed:Success ratio = "+str(failed)+":"+str(success)+"\n")
    f.close()
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
print("the following files exist on the SD-Card.\n"+str(os.listdir('/sd')))
