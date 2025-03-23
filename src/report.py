import ilog
import battery
import orientation
import datetime
import witty.witty as witty
import config
import unicodedata
import re
import os

def slugify(value, allow_unicode=True):
	"""
	Taken from https://github.com/django/django/blob/master/django/utils/text.py
	Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
	dashes to single dashes. Remove characters that aren't alphanumerics,
	underscores, or hyphens. Convert to lowercase. Also strip leading and
	trailing whitespace, dashes, and underscores.
	"""
	value = str(value)
	if allow_unicode:
		value = unicodedata.normalize('NFKC', value)
	else:
		value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
	value = re.sub(r'[^\w\s-]', '', value.lower())
	return re.sub(r'[-\s]+', '-', value).strip('-_')

def report(art):
	now = datetime.datetime.now()
	try:
		secs = str(now.timestamp())
		if not os.path.exists(config.current.pictures_directory):
			os.makedirs(config.current.pictures_directory)
		
		jpg = art.original_image.convert("RGB")
		jpg.save(config.current.pictures_directory + "/" + slugify(art.image_name) + "_" + secs + ".jpg")
	except Exception as e:
		ilog.log(e)

	try:
		ilog.log(f"datetime: {now}")
		ilog.log(f"get_battery_percentage: {battery.get_battery_percentage()}%")
		ilog.log(f"battery_low? {battery.battery_low()}")
		ilog.log(f"orientation: {orientation.get()}")
		ilog.log(f"image_name: {art.image_name}")
		ilog.log(f"image_source: {art.image_source}")
		ilog.log(f"image_url: {art.image_url}")
		ilog.log(f"refresh_mode: {config.current.refresh_mode}")
		ilog.log(f"auto_shutdown: {config.current.auto_shutdown}")
		ilog.log(f"scheduled_shutdown: {witty.get_shutdown_time()}")
		ilog.log(f"scheduled_startup: {witty.get_startup_time()}")
	except Exception as e:
		ilog.log(e)
		pass
	ilog.log("==========================================")
	ilog.dump()
