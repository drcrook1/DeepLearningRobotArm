import serial
import time
#ser = serial.Serial('/dev/ttyUSB0', 9600)
ser = serial.Serial('/dev/ttyACM0', 9600)


while 1 :
	print(ser.readline())
	#user.write('0,90,14,-90')
	#time.sleep(2)
	#ser.write('0,90,14,45')
