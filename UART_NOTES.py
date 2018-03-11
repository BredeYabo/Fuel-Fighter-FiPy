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
