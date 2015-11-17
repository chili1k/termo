import sqlite3
import urllib
import xml.etree.ElementTree as ET
import tempfile
import commands
import os

def getoutsidetemp(arsourl,arsocity):
	f = urllib.urlopen('{0}/{1}'.format(arsourl,arsocity))
	root = ET.parse(f).getroot()
	temp = float(root.find('metData').find('t_degreesC').text)
	return round(temp,2);


def get_graphimage(sensorid,starttime,endtime):
	ftmp,tmpfile = tempfile.mkstemp(suffix='.png')
	
	cmd = (('rrdtool graph {3} --start \'{1}\' --end \'{2}\' --vertical-label Temperatura '+
	                        '--width 500 --height 200 --slope-mode DEF:temp=./rrd/sensor{0}.rrd:temp:AVERAGE '+
				'LINE:temp#ff0000:Temperatura').
		format(sensorid, starttime, endtime, tmpfile))
	ret = commands.getstatusoutput(cmd)

	try:
		if ret[0] != 0:
		        raise Exception('Error creating rrd graph: {0}. Error code: {1}. sensorid: {2}, starttime: {3}, endtime: {4}. cmd: {5}'.
		                format(ret[1], ret[0], sensorid, starttime, endtime, cmd))
		else:
			f = open(tmpfile,'r')
			img = f.read()
			f.close()
			return img
	finally:
		os.remove(tmpfile)


class termoconf():
	rocommunity = None;
	rwcommunity = None;
	boardhostname = None;
	arsourl = None
	arsocity = None

	def __get_setting(self,c,key):
		c.execute('SELECT value FROM settings WHERE key = ?', [key])
		return c.fetchone()[0];

	def __init__(self, conn):
		c = conn.cursor()
		self.rocommunity = self.__get_setting(c,'rocommunity').encode('utf-8')
		self.rwcommunity = self.__get_setting(c,'rwcommunity').encode('utf-8')
		self.boardhostname = self.__get_setting(c,'boardhostname').encode('utf-8')
		self.arsourl = self.__get_setting(c,'arsourl').encode('utf-8')
		self.arsocity = self.__get_setting(c,'arsocity').encode('utf-8')

#class sensor():
#	sensorid = None;
#	name = None;
#	comment = None;
#	automatic = None;
#	temperature = None;
#	threshold = None;
#	enabled = None;
#	relayid = None;
#	updatetime = None;
#	__conn = None;
#
#	def __readrowdata(self,row):
#		if row:
#			self.sensorid = row['sensorid'];
#		        self.name = row['name'];
#		        self.comment = row['comment'];
#		        self.automatic = row['automatic'];
#		        self.temperature = row['temperature'];
#		        self.threshold = row['threshold'];
#		        self.enabled = row['enabled'];
#		        self.relayid = row['relayid'];
#	
#	def __init__(self,conn):
#		self.__conn = conn;
#
#	def __init__(self,conn,sensorid):
#		conn.row_factory = sqlite3.Row
#		c = conn.cursor()
#		c.execute('SELECT sensorid,name,comment,automatic,temperature,threshold,'+
#			'enabled,relayid,updatetime FROM sensors WHERE sensorid = ?', [sensorid])
#		row = c.fetchone()
#		self.__readrowdata(row)
#
#        def __init__(self,conn):
#                conn.row_factory = sqlite3.Row
#                c = conn.cursor()
#                c.execute('SELECT sensorid,name,comment,automatic,temperature,threshold,'+
#                        'enabled,relayid,updatetime FROM sensors')
#                row = c.fetchone()
#                self.__readrowdata(row)
