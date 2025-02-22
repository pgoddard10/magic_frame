from epaper.drivers import epd7in3f

def get_width():
	return epd7in3f.EPD_WIDTH

def get_height():
	return epd7in3f.EPD_HEIGHT

def display(img):
	print("Attempting to refresh the image in waveshare_7_3_epd.py")
	try:
		epd = epd7in3f.EPD()
		epd.init()
		epd.Clear()
		epd.display(epd.getbuffer(img))
		epd.sleep()
		print("Display updated")

	except IOError as e:
		print(e)

	except:
		print("Exception in waveshare_7_3_epd.py")
		epd7in3f.epdconfig.module_exit()
