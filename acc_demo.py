import sense_hat
import time, sys






led = sense_hat.LedMatrix()
led.clear()

pr = sense_hat.Sensor(0x6a)
pr.write(0x20, 0b11000000)

slid_x = []
slid_y = []

while len(slid_x) < 128:
	data = pr.read(0x28) | pr.read(0x29) << 8
	data -= (data & 1<<15)*2
	slid_x.append(data)

calib_x = reduce(lambda x,y: x+y, slid_x)*1.0/len(slid_x)


while len(slid_y) < 128:
	data = pr.read(0x2A) | pr.read(0x2B) << 8
	data -= (data & 1<<15)*2
	slid_y.append(data)

calib_y = reduce(lambda x,y: x+y, slid_y)*1.0/len(slid_y)

slid_x = []
slid_y = []

while 1:
	data_x = pr.read(0x28) | pr.read(0x29) << 8
	data_x -= (data_x & 1<<15)*2

	data_y = pr.read(0x2A) | pr.read(0x2B) << 8
	data_y -= (data_y & 1<<15)*2



	while len(slid_x) > 2: del slid_x[0]
	slid_x.append(data_x)

	while len(slid_y) > 2: del slid_y[0]
	slid_y.append(data_y)


	avg_x = reduce(lambda x,y: x+y, slid_x)*1.0/len(slid_x) - calib_x
	avg_y = reduce(lambda x,y: x+y, slid_y)*1.0/len(slid_y) - calib_y


	sys.stdout.write("\r\t{:0.2f} \t{:0.2f}   ".format(avg_x/2500.0, avg_y/2500.0) )
	sys.stdout.flush()


	pixl_x = int(avg_x/2500.0+4)
	pixl_y = int(avg_y/2500.0+4)

	led.set_pixel( pixl_y, pixl_x, (0,255,255) )
	led.fb_flush()
	time.sleep(0.005)
