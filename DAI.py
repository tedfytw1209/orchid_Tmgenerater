import time, random, requests, threading
import DAN
import numpy as np
import datetime


ServerURL = 'http://iot.iottalk.tw:9999'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = 'OrchidTm_generater' #if None, Reg_addr = MAC address
ODF_list = ['Temperature-O1','Temperature-O6','Humidity-O6']
IDF_list = ['Settemp-I1'] #Tm output

DAN.profile['dm_name']='Orchidhouse_control'
DAN.profile['df_list']=ODF_list+IDF_list
DAN.profile['d_name']= 'OrchidTm_generater01' 

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line

#DAI feature & Variable
T24_form = '%H:%M'
Time_from = '%Y-%m-%d %H:%M'
Time_interval = 10
Tm_output = 26
Tm_record_file = 'Tm.txt'
Alpha = 0.8
Day_data = []

#function
def Tm_addup(temp_avg):
    new_tm = (1-Alpha)*temp_avg + Alpha*Tm_output
    return new_tm

def get_slice_time(time_obj):
    hour = time_obj.hour
    min = time_obj.minute
    return int((hour*60+min)/Time_interval)*Time_interval

#EN15251 role
def comfort_temp(outside_temp):
    return (outside_temp+56)/3
    
Now_date = datetime.datetime.today()
Past_date = Now_date
#try to read Tm first
try:
    f = open(Tm_record_file,'r')
    tmp = float(f.read())
    if tmp < 35 and tmp > 10 and tmp:
        Tm_output = tmp
    f.close()
except Exception as e:
    print('Warning :')
    print(e)
#main
while True:
    Last_time = time.time()
    try:
        Now_date = datetime.datetime.today()
        #get data
        temp = DAN.pull('Temperature-O1')
        if temp:
            Day_data.append(temp[0])
            
        if (Now_date.day != Past_date.day):
            print(Now_date)
            print('update Trm temperature')
            tmp_temp = np.average(np.array(Day_data))
            Tm_output = Tm_addup(tmp_temp)
            print(Tm_output)
            #DAN.push('Settemp-O1',Tm_output)
            Day_data = []
            #save current data
            f = open(Tm_record_file,'w')
            f.write(str(Tm_output))
            f.close()
        DAN.push('Settemp-I1',Tm_output)
        Past_date = Now_date
    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    
    #sleep
    time.sleep(60 - ((time.time() - Last_time) % 60)) #a minute check once
    

