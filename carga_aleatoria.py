'''
Carga 1 v2
Moneda: Monero
Algoritmo: cryptonight
Tiempo minando: aleatorio 
Tiempo dormido: aleatorio
Threads: aleatorio
Ejecución paralela: aleatoria
'''
from random import randint, choice
import time
import os

def carga:
	for x in range(1,5):
		minando = randint(60, 300)
		dormido = randint(10, 60)
		threads = randint(1, 4)
		minerd = "sudo ./minerd -a cryptonight -o stratum+tcp://xmr.pool.minergate.com:45700 -u sergipm11@hotmail.com -p X -t " + str(threads) + " -B"
		os.system(minerd)
		time.sleep(minando)
		os.system("sudo pkill minerd")
		time.sleep(dormido)

def frecuencia:
	formato = choice(["userspace", "ondemand"])
	if(formato == "ondemand"):
		os.system("sudo cpufreq-set -r -g ondemand")
	else:
		frec = choice(["1.4Ghz", "600Mhz"])
		os.system("sudo cpufreq-set -r -g userspace")
		os.system("sudo cpufreq-set -r -f " + frec)

while(True):
	frecuencia()
	carga()





