    if ((time//1000))!=acc_count:
        acc_count=(time//1000)
        pitch = acc.pitch()
        roll = acc.roll()
        time=time_c(str(time))
        r_v=time+sp+str(pitch)+sp+str(roll)
        CANID='acc'
        temp=acc_file
        store(CANID,r_v)
        acc_file=temp
        continue

    try:
        f=open('/sd/update.txt','r')
        line=f.read()
        f.close()
    except:
        line="No .txt file found"

    while c<1000:
        while c<100:
            c+=1
            ts(0.01)
            GNDL.value(1)
            GNDR.value(0)
            PWR.value(1)
            ts(0.01)
            PWR.value(1)
            GNDL.value(0)
            GNDR.value(1)
        while c<200:
            c+=1
            ts(0.01)
            GNDL.value(1)
            GNDR.value(0)
            PWR.value(1)
            ts(0.01)
            PWR.value(0)
            GNDL.value(0)
            GNDR.value(1)
        while c<300:
            c+=1
            ts(0.01)
            GNDL.value(1)
            GNDR.value(0)
            PWR.value(0)
            ts(0.01)
            PWR.value(0)
            GNDL.value(0)
            GNDR.value(1)
        while c<400:
            c+=1
            ts(0.01)
            GNDL.value(1)
            GNDR.value(0)
            PWR.value(0)
            ts(0.01)
            PWR.value(1)
            GNDL.value(0)
            GNDR.value(1)
        while c<500:
            c+=1
            ts(0.01)
            GNDL.value(1)
            GNDR.value(0)
            PWR.value(1)
            ts(0.01)
            PWR.value(1)
            GNDL.value(0)
            GNDR.value(1)
        while c<600:
            c+=1
            ts(0.01)
            GNDL.value(1)
            GNDR.value(0)
            PWR.value(1)
            ts(0.01)
            PWR.value(0)
            GNDL.value(0)
            GNDR.value(1)
        while c<700:
            c+=1
            ts(0.01)
            GNDL.value(1)
            GNDR.value(0)
            PWR.value(0)
            ts(0.01)
            PWR.value(0)
            GNDL.value(0)
            GNDR.value(1)
        while c<800:
            c+=1
            ts(0.01)
            GNDL.value(1)
            GNDR.value(0)
            PWR.value(0)
            ts(0.01)
            PWR.value(1)
            GNDL.value(0)
            GNDR.value(1)
        while c<900:
            c+=1
            ts(0.01)
            GNDL.value(1)
            GNDR.value(0)
            PWR.value(1)
            ts(0.01)
            PWR.value(1)
            GNDL.value(0)
            GNDR.value(1)
        while c<1000:
            c+=1
            ts(0.01)
            GNDL.value(1)
            GNDR.value(0)
            PWR.value(1)
            ts(0.01)
            PWR.value(0)
            GNDL.value(0)
            GNDR.value(1)
        while c<1100:
            c+=1
            ts(0.01)
            GNDL.value(1)
            GNDR.value(0)
            PWR.value(0)
            ts(0.01)
            PWR.value(0)
            GNDL.value(0)
            GNDR.value(1)
        while c<1200:
            c+=1
            ts(0.01)
            GNDL.value(1)
            GNDR.value(0)
            PWR.value(0)
            ts(0.01)
            PWR.value(1)
            GNDL.value(0)
            GNDR.value(1)
    GNDL.value(0)#GND Left
    PWR.value(0)#PWR
    GNDR.value(0)#GND right
