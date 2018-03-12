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
