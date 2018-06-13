'''
Carga 1 v2
Moneda: Monero
Algoritmo: cryptonight
Tiempo minando: 300, 120
Tiempo dormido: 60, 30
Threads: variables de 1 a 4
Ejecución paralela (A=apagado, E=encendido):
1-> A E A E
3-> E E E E
5-> A A E E
Tiempo total = 4.8 + 2 = 6.8 horas
'''
import time
import os

def carga:
	for threads in range(1,5):
		minerd = "sudo ./minerd -a cryptonight -o stratum+tcp://xmr.pool.minergate.com:45700 -u sergipm11@hotmail.com -p X -t " + str(threads) + " -B"
		os.system(minerd)
		time.sleep(minando)
		os.system("sudo pkill minerd")
		time.sleep(dormido)

i, j = 0, 0
minando = 300
dormido = 60
os.system("sudo cpufreq-set -r -g userspace")
os.system("sudo cpufreq-set -r -f 1.4Ghz")
#time.sleep((minando+dormido)*4)

while(True):
	if(i%4==0):
		carga()
	elif(i%4==1):
		carga()
	elif(i%4==2):
		carga()
	elif(i%4==3):
		carga()
		j = j + 1
		if(j>2):
			minando = 120
			dormido = 30
		if(j%3==0):
			os.system("sudo cpufreq-set -r -g userspace")
			os.system("sudo cpufreq-set -r -f 1.4Ghz")
		elif(j%3==1):
			os.system("sudo cpufreq-set -r -g userspace")
			os.system("sudo cpufreq-set -r -f 6OOMhz")
		elif(j%3==2):
			os.system("sudo cpufreq-set -r -g ondemand")
	i = i + 1

