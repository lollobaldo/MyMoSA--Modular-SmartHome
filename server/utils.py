import logging
import threading, time, traceback
import sqlite3

def my_logger (mqtt_client , channel , msg):
	print(msg)
	#mqtt_client.publish(channel , msg , 2 , True)
	logging.info(msg)

def every(delay, task):
  next_time = time.time() + delay
  while True:
    time.sleep(max(0, next_time - time.time()))
    try:
      task()
    except Exception:
      traceback.print_exc()
      # in production code you might want to have this instead of course:
      # logger.exception("Problem while executing repetitive task.")
    # skip tasks if we are behind schedule:
    next_time += (time.time() - next_time) // delay * delay + delay

def execute_every(task, delay):
	task()
	print("registering task")
	threading.Thread(target=lambda: every(delay , task)).start()

def db_insert(query, args):
	db = sqlite3.connect("DB.sqlite")
	cursor = db.cursor()
	print(query)
	try:
		cursor.execute(query, args)
		db.commit()
	except Exception as e:
		# Roll back any change if something goes wrong
		db.rollback()
		raise e
	finally:
		# Close the db connection
		db.close()

def resetDB():
	db = sqlite3.connect("DB.sqlite")
	cursor = db.cursor()
	cursor.execute("""
		CREATE TABLE DHT(
			date INTEGER PRIMARY KEY,
			humidity INTEGER,
			temperature INTEGER)""")
	cursor.execute("""
		CREATE TABLE systemStats(
			date INTEGER PRIMARY KEY,
			cpu TEXT,
			mem_avail INTEGER,
			disk_free INTEGER,
			net_sent REAL,
			net_recv REAL,
			temp REAL)""")
	db.commit()
	db.close()