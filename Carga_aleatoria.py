# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 13:02:39 2018

@author: Sergio

"""

from random import randint
from numpy.random import choice
import time, os

#Variables
raspi=[0,0,0,0,0,0]
anterior=[0,0,0,0,0,0]
#Parametros
tmin, tmax = 1, 10
umbral_fmax = 5
prob_600Mhz, prob_1Ghz = 0.3, 0.7

def numero_raspis():
    global raspi
    for i in range(len(raspi)):
        raspi[i] = randint(0,1)
    
def frecuencia():
    if(raspi.count(1)>=umbral_fmax):
        for i in range(1, len(raspi)):
            frecuencia = choice(["600Mhz", "1.4Ghz"], 1, p=[prob_600Mhz, prob_1Ghz])
            os.system("ssh pi@10.40.38.10" + str(i+1) + " 'sudo cpufreq-set -r -f " + frecuencia[0] + "'")
        frecuencia = choice(["600Mhz", "1.4Ghz"], 1, p=[prob_600Mhz, prob_1Ghz])
        os.system("sudo cpufreq-set -r -f " + frecuencia[0])
    else:
        for i in range(1, len(raspi)):
            os.system("ssh pi@10.40.38.10" + str(i+1) + " 'sudo cpufreq-set -r -f 1.4Ghz'")
        os.system("sudo cpufreq-set -r -f 1.4Ghz")

def encendido():
    for i in range(1,len(raspi)):
        if(raspi[i]==True and anterior[i]==False): #Para las rasi esclavas
            os.system("ssh pi@10.40.38.10" + str(i+1) + " 'sudo python minar.py' &")
        elif(raspi[i]==False and anterior[i]==True):
            os.system("ssh pi@10.40.38.10" + str(i+1) + " 'sudo pkill minerd'")
    if(raspi[0]==True and anterior[0]==False): #Para la raspi master
        os.system("sudo /home/pi/cpuminer-multi/minerd -a cryptonight -o stratum+tcp://bcn.pool.minergate.com:45550 -u sergipm11@hotmail.com -p X -t 4 -B")
    elif(raspi[0]==False and anterior[0]==True):   
        os.system("sudo pkill minerd")  
        
def dormir():
    global anterior
    for i in range(len(raspi)):
        anterior[i]=raspi[i]
    time.sleep(randint(tmin, tmax))

while(True):
    numero_raspis()
    frecuencia()
    encendido()
    dormir()
