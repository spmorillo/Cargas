# -*- coding: utf8 -*-
import collectd
from subprocess import check_output
from re import search

#Parsed metrics array
metrics = []

def power():
        power_result = check_output(['/root/rapl-read/rapl-read | grep package-'], shell=True).split('\n')[:-1]
        for i in range(len(power_result)):
                power_name = "Socket" + str(i)
                string = ": (.*)J"
                match = search(string, power_result[i])
                metrics.append([power_name, float(match.group(1)[:6]), 'power'])

def temp_cores():
        temp_result = check_output(['sensors'], shell=True).split("coretemp")[1:]
        for i in range(len(temp_result)):
                cores = temp_result[i].count("Core")
                for j in range(cores):
                        temp_name = "Core" + str(j+(i*cores))
                        string = "Core " + str(j) + ":         [+]+(.*)°C  " #It's not º but °
                        match = search(string, temp_result[i])
                        metrics.append([temp_name, match.group(1), 'temperature'])

def temp_mem_volt_fan():
        fan_mem_result = filter(None, check_output(['ipmitool sdr'], shell=True).split('\n'))
        find, metric_index = 0, [0,0,0]
        for i in range(len(fan_mem_result)):
                if("Mem Slot" in fan_mem_result[i]):
                        name, type_val, find, metric_index[0] = 'Memory'+ str(metric_index[0]), 'temperature', 1, metric_index[0]+1
                elif("PVCCP" in fan_mem_result[i]):
                        name, type_val, find, metric_index[1] = 'Socket'+str(metric_index[1]), 'voltage', 1, metric_index[1]+1
                elif("Fan Tach" in fan_mem_result[i]):
                        name, type_val, find, metric_index[2] = 'Fan'+str(metric_index[2]), 'fanspeed', 1, metric_index[2]+1
                if(find==1 or find==2):
                        if(find==2):
                                value = float(filter(None, fan_mem_result[i].split(' '))[3])*1000
                        else:
                                value = float(filter(None, fan_mem_result[i].split(' '))[3])
                        find = 0
                        metrics.append([name,value,type_val])

def freq():
        freq_result = check_output(['cat /proc/cpuinfo | grep MHz'], shell=True).split('\n')[:-1]
        for i in range(len(freq_result)):
                freq_name = 'Core' + str(i)
                string = "cpu MHz\t\t: (.*)"
                match = search(string, freq_result[i])
                metrics.append([freq_name, match.group(1), 'clock'])

def util():
        util_result = check_output(['mpstat -P ALL'], shell=True).split('\n')[4:-1]
        for i in range(len(util_result)):
                core = filter(None, util_result[i].split(' '))
                util_name = "Core" + str(i) + "."
                metrics.append([util_name+"user", float(core[3]), 'utilization'])
                metrics.append([util_name+"nice", float(core[4]), 'utilization'])

def read():
        global metrics
        temp_cores(), temp_mem_volt_fan(), freq(), util(), power()
        val = collectd.Values()
        for i in range(len(metrics)):
                val.meta = {"index": i}
                val.plugin = metrics[i][0]
                val.type = metrics[i][2]
                val.values = [metrics[i][1]]
                val.dispatch()
        metrics = []

collectd.register_read(read,10)
