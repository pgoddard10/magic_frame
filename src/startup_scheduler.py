import witty.witty as witty
import config
import subprocess
import datetime


def sync_rtc_time():
	now = datetime.datetime.now()
	print(f"Current time: {now}")
	witty.set_rtc_datetime(now)

def is_time_to_sleep(time):
	no_updates_from = datetime.datetime.strptime(config.current.no_updates_from, "%H:%M").time()
	no_updates_to = datetime.datetime.strptime(config.current.no_updates_to, "%H:%M").time()

	# Check if the 'no_updates_to' time is earlier than 'no_updates_from' (i.e., crosses midnight)
	if no_updates_to < no_updates_from:
		# If so, consider the 'no_updates_to' as being on the next day
		if no_updates_from <= time.time() or time.time() <= no_updates_to:
			return True
	else:
		# Normal case: no crossing midnight
		if no_updates_from <= time.time() <= no_updates_to:
			return True
		
	return False

def schedule_next_startup():
	now = datetime.datetime.now()	

	if config.current.refresh_mode == "hourly":
		time = now + datetime.timedelta(hours = 1)
		time = time.replace(minute = 0, second = 0)

		# check if the new time is between the no_updates_from and no_updates_to
		# times in the config file. If the new time is, override the time with
		# the no_updates_to time
		if(is_time_to_sleep(time)):
			time = now + datetime.timedelta(days = 1)
			split = config.current.no_updates_to.split(":")
			time = time.replace(
				hour = int(split[0]), 
				minute = int(split[1]), 
				second = 0
			)

	elif config.current.refresh_mode == "debug":
		time = now + datetime.timedelta(
			hours = 0, 
			minutes = 3, 
			seconds = 0
		)
	else:
		time = now + datetime.timedelta(days = 1)
		split = config.current.daily_refresh_time.split(":")
		time = time.replace(
			hour = int(split[0]), 
			minute = int(split[1]), 
			second = 0
		)
	
	witty.set_startup_time(time)
	print(f"Scheduled startup to {witty.get_startup_time()}")


def schedule_shutdown(min = 0, sec = 5):
	if not config.current.auto_shutdown:
		print(f"Shutdown scheduling disabled.")
		return
	now = datetime.datetime.now()
	shutdown = now + datetime.timedelta(minutes = min, seconds = sec)
	witty.set_shutdown_time(shutdown)
	print(f"Scheduled shutdown to {witty.get_shutdown_time()}")
