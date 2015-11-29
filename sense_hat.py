''' Raspberry Pi SenseHAT library '''


try:
	import smbus
except:
	raise Exception("This module requires smbus")



class LedMatrix:
	fb = [0x00] * 192

	def __init__(self, address=ADDR_USER_IO):
		self.ctrl_address = address
		self.i2cbus = smbus.SMBus(1)

	def clear(self):
		for i in range(0,192,32):
			self.i2cbus.write_i2c_block_data(self.ctrl_address, i, [0]*32)

	def set_pixel(self, x, y, color):
		x = max(min(x, 7), 0)
		y = max(min(y, 7), 0)
		self.fb[x*24+y   ] = max(min(color[0],63),0)
		self.fb[x*24+y+8 ] = max(min(color[1],63),0)
		self.fb[x*24+y+16] = max(min(color[2],63),0)
		return False

	def set_pixel_direct(self, x,y, color):
		self.i2cbus.write_byte_data(self.ctrl_address, x*24+y, color[0])
		self.i2cbus.write_byte_data(self.ctrl_address, x*24+y+8, color[1])
		self.i2cbus.write_byte_data(self.ctrl_address, x*24+y+16, color[2])
		return False

	def fb_flush(self):
		for i in range(0,192,32):
			self.i2cbus.write_i2c_block_data(self.ctrl_address, i, self.fb[i:i+32])
		self.fb = [0x00] * 192




class DPad:
	def __init__(self, address=ADDR_USER_IO):
		self.ctrl_address = address
		self.i2cbus = smbus.SMBus(1)

	def get_state(self):
		joy = self.i2cbus.read_byte_data(self.ctrl_address, 0xF2)
		down = joy & 1 != 0
		right = joy & 0b10 != 0
		up = joy & 0b100 != 0
		left = joy & 0b10000 != 0
		push = joy & 0b1000 != 0

		return up, down, left, right, push

class Sensor:
	def __init__(self, address):
		self.i2cbus = smbus.SMBus(1)
		self.ctrl_address = address


	def write(self, a, d):
		self.i2cbus.write_byte_data(self.ctrl_address, a, d)
	def read(self, a):
		return self.i2cbus.read_byte_data(self.ctrl_address, a)
