import time, random, requests, threading
import DAN
import numpy as np
import datetime


ServerURL = 'http://iot.iottalk.tw:9999'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = None #if None, Reg_addr = MAC address
ODF_list = ['CO2-O','Temperature-O1','Temperature-O6','Humidity-O6']
IDF_list = ['Settemp-O1'] #Tm output

DAN.profile['dm_name']='Orchidhouse_control'
DAN.profile['df_list']=ODF_list+IDF_list
DAN.profile['d_name']= 'OrchidTm_generater' 

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line

#DAI feature
T24_form = '%H:%M'
Time_from = '%Y-%m-%d %H:%M'
Time_interval = 10
Tm_output = 26
Tm_record_file = 'Tm.txt'

#function
def Tm_addup(temp_avg):
    

def get_slice_time(time_obj):
    hour = time_obj.hour
    min = time_obj.minute
    return int((hour*60+min)/Time_interval)*Time_interval

#EN15251 role
def comfort_temp(outside_temp):
    return (outside_temp+56)/3

#thread function 1 : constantly change settemp by model predict
def model_settemp():
    #var
    co2 = DAN.pull('CO2-O')
    temp_out = DAN.pull('Temperature-O1')
    temp_house = DAN.pull('Temperature-O6')
    humidity = DAN.pull('Humidity-O6')
    settemp1 = DAN.pull('Settemp-O1')
    settemp2 = DAN.pull('Settemp-O2')
    Setted_temperature = (settemp1+settemp2)/2
    #pass
    
    #push
    
#thread function 2 : change settemp by voting result
def pullVoting(option_id,option_index):
    Option = DAN.pull(option_id)
    if Option = 1.0:
        
    
#variable
voted = False
#main
while True:
    Last_time = time.time()
    try:
        
    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    
    #action push
    for act in ACTION_SET:
        DAN.push(act,Actions[act])
    #sleep
    time.sleep(60 - ((time.time() - Last_time) % 60)) #a minute check once
    

