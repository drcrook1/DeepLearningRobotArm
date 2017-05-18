import picamera
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)

counter = 0

while 1 :
	line = ser.readline()
	print(line)
        with picamera.PiCamera() as camera:
		camera.vflip = True
		camera.hflip = True
		camera.capture('./capture/image' + str(counter) + '.jpg')
    	file = open("./capture/data" + str(counter) + ".txt", "w")
    	file.write(line)
    	counter += 1



    
