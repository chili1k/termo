#/usr/bin/python

import commands
import syslog
import logging
import logging.config
import time
import sqlite3
import os
import sys
from daenetip import *
from termoutil import *

def writedata(sensorid,temperature):
	rrdname = 'sensor'+str(sensorid)+'.rrd'
	rrdlastname = 'sensor'+str(sensorid)+'last.rrd'
	ret = commands.getstatusoutput('rrdtool update ./rrd/sensor{0}.rrd N:{1}'.format(sensorid,temperature))
        ret = commands.getstatusoutput('rrdtool update ./rrd/sensor{0}last.rrd N:{1}'.format(sensorid,temperature))
        if ret[0] != 0:
	          logging.error('Error writing temperature to rrd: '+ret[1]+'. Temperature: '+str(temperature)+'. Error code '+str(ret[0]))
	return ret[0]

def makegraph(sensorid, sensorname, _starttime = None, _endtime = None):
	if _starttime is None:
		# 1 week in the past
		startTime = 'end-43200'
	else:
		startTime = _starttime

	if _endtime is None:
		endTime = 'now'
	else:
		endTime = _endtime

	logging.debug('Creating graph from data. Start: {0}, End: {1}'.format(startTime, endTime))
	cmd = ('rrdtool graph ./static/img/sensor{0}.png --start \'{1}\' --end \'{2}\' --vertical-label Temperatura '+
                                '--width 500 --height 200 --slope-mode DEF:temp=./rrd/sensor{0}.rrd:temp:AVERAGE '+
                                'LINE:temp#ff0000:\'{3}\'').format(sensorid, startTime, endTime, sensorname.encode('utf-8')) 
	ret = commands.getstatusoutput(cmd)

	if ret[0] != 0:
		logging.error('Error creating rrd graph: {0}. Error code: {1}. sensorid: {2}, sensorname: {3}, starttime: {4}, endtime: {5}'.
			format(ret[1], ret[0], sensorid, sensorname, startTime, endTime))
	else:
		logging.debug('Graph created successfully!')



FORMAT='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT,level=logging.DEBUG)

# Change working directory to script path
scriptPath = os.path.dirname(os.path.realpath(__file__)) 
os.chdir(scriptPath)

conn = sqlite3.connect('termo.db')
conf = termoconf(conn)
daenet = daenetip(conf.boardhostname)

try:
	for sensor in conn.execute('SELECT sensorid,name,threshold,relayid,automatic FROM sensors WHERE enabled = 1'): 
		sensorid = sensor[0]
		sensorname = sensor[1]
		threshold = sensor[2]
		relayid = sensor[3]
		automatic = sensor[4]

		logging.debug('Retrieving temperature from module '+conf.boardhostname)
		temperature = daenet.gettemp(sensorid)
		logging.debug('Retrieved temparature: {0}'.format(temperature))
		logging.debug('Writing temperature to database ...')
		
		conn.execute('UPDATE sensors SET temperature = ?, updatetime=datetime(current_timestamp, \'localtime\') '+
				'WHERE sensorid=?', [temperature,sensorid])
		if temperature is not None:
			logging.debug('Logging sensor {0} temperature.'.format(sensorid))
			writedata(sensorid, temperature)

		if automatic:
			if temperature <= threshold:
				logging.debug('Temperature is below threshold {0}. Turning relay {1} ON.'.format(threshold, relayid))
				daenet.setrelay(relayid,1)
			else:
				logging.debug('Temperature is above threshold {0}. Turning relay {1} OFF.'.format(threshold, relayid))
				daenet.setrelay(relayid,0)
		else:
			logging.debug('Sensor is not set to automatic. Skipping relay configuration.')

		logging.debug("Drawing graph for sensor "+sensorname)
		#makegraph(sensorid, sensorname, 'end-43200','now')
except sqlite3.Error as e:
	logging.error('Error reading sensor data from SQL: '+e[0])

conn.commit()
conn.close()
