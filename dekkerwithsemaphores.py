# -*- coding: utf-8 -*-
from multiprocessing import Process
from multiprocessing import current_process
from multiprocessing import Value, Array
from multiprocessing import BoundedSemaphore

N = 8


def task(common,tid,l):
	a = 0
	for i in range(100):
		print(f'{tid}−{i}: Non−critical Section')
		a += 1
		print(f'{tid}−{i}: End of non−critical Section')
		l.acquire()
		try:
			print(f'{tid}−{i}: Critical section')
			v = common.value + 1
			print(f'{tid}−{i}: Inside critical section')
			common.value = v
			print(f'{tid}−{i}: End of critical section')
		finally:
			l.release()

def main():
	sem=BoundedSemaphore(1) #Utilizamos un semaforo con de uno solo, si se aumenta el numero de elementos en el semaforo, dos procesos pueden entrar en la sección crítca a la vez y el programa pierde determinismo
	lp = []
	common = Value('i', 0)
	for tid in range(N):
		lp.append(Process(target=task, args=(common, tid, sem)))
	print (f"Valor inicial del contador {common.value}")
	for p in lp:
		p.start()
	for p in lp:
		p.join()
	print (f"Valor final del contador {common.value}")
	print ("fin")
if __name__ == "__main__":
	main()