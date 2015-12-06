import sqlite3
from bottle import route, debug, template, run, static_file, get, post, request, response
from daenetip import *
from termoutil import *
from time import mktime
from datetime import datetime,timedelta

def get_sensors(conn):
	c = conn.cursor()
	c.execute('SELECT sensorid,name FROM sensors')
	return c.fetchall()

def get_sensor(sensorid,conn):
	c = conn.cursor()
	if sensorid is not None:
		c.execute('SELECT s.sensorid,s.name,s.comment,s.threshold,s.temperature,s.automatic,'+
			's.enabled,s.updatetime,s.relayid,r.state relaystate FROM sensors s '+
			'LEFT JOIN relays r on s.relayid = r.relayid '
			'WHERE sensorid=?', [sensorid])
		sensordata = c.fetchone()
	else:
		# Select first enabled sensor if no id is gived
		c.execute('SELECT s.sensorid,s.name,s.comment,s.threshold,s.temperature,s.automatic,'+
						's.enabled,s.updatetime,s.relayid,r.state relaystate FROM sensors s '+
						'LEFT JOIN relays r on s.relayid = r.relayid LIMIT 1')
		sensordata = c.fetchone()
	return sensordata

@route('/')
@route('/sensor/<sensorid:int>')
def sensor(sensorid = None):
	conn = sqlite3.connect('termo.db')
	conn.row_factory = sqlite3.Row

	sensordata = get_sensor(sensorid,conn)
	sensors = get_sensors(conn)
	#sensorgraph = '/static/img/sensor'+str(sensordata['sensorid'])+'.png'
	conf = termoconf(conn)
	outsidetemp = getoutsidetemp(conf.arsourl,conf.arsocity)
	daenet = daenetip(conf.boardhostname, conf.appmode)
	# When developing read relay state from DB
	if conf.appmode == "dev":
		relaystate = sensordata['relaystate'];
	else:
		relaystate = daenet.getrelay(sensordata['relayid'])	
	endtime = datetime.now()
	starttime = (datetime.now() - timedelta(hours=12))
	sensorgraph = '/graph?sensorid={0}&start={1}&end={2}'.format(sensordata[0],
	starttime.strftime('%Y%m%d%H%M'),endtime.strftime('%Y%m%d%H%M'))

	conn.close()
	return template('sensor_template',sensor=sensordata,sensorgraph=sensorgraph,sensors=sensors,
		outsidetemp=outsidetemp,relaystate=relaystate,starttime=starttime,endtime=endtime,activepage='overview')

@route('/sensor/edit/<sensorid:int>')
def edit_sensor(sensorid = None):
	conn = sqlite3.connect('termo.db')
	conn.row_factory = sqlite3.Row

	sensordata = get_sensor(sensorid,conn)
	sensors = get_sensors(conn)

	conn.close()
	return template('sensor_edit_template',sensor=sensordata,sensors=sensors,activepage='setup')

@route('/relay/toggle/<relayid:int>', method='get')
def toggle_sensor(relayid = None):
	conn = sqlite3.connect('termo.db')
	relaystate = conn.execute('SELECT state FROM relays WHERE relayid = ?', [relayid]).fetchone()[0]
	if relaystate:
		newstate = 0
	else:
		newstate = 1

	conf = termoconf(conn)
	daenet = daenetip(conf.boardhostname, conf.appmode)	
	daenet.setrelay(relayid,newstate)
	conn.execute('UPDATE relays SET state = ?',[newstate])
	conn.commit()
	conn.close()
	sensorid = request.GET.get('sensorid','')
	return sensor(sensorid)

@route('/sensor/save/<sensorid:int>', method='POST')
def save_sensor(sensorid):
	name = request.POST.get('name','').strip().decode('utf-8')
	comment = request.POST.get('comment','').strip().decode('utf-8')
	threshold = int(request.POST.get('threshold',''))
	automatic = int(request.POST.get('automaticmode',''))
	enabled = int(request.POST.get('enabled','0'))

	conn = sqlite3.connect('termo.db')
	conn.execute('UPDATE sensors SET enabled=?,name=?,comment=?,threshold=?,automatic=? WHERE sensorid=?',
		[enabled,name,comment,threshold,automatic,sensorid])
	conn.commit()
	conn.close()
	return edit_sensor(sensorid) 

@route('/graph')
def get_graph():
	response.headers['Content-Type'] = 'image/png'
	response.headers['Content-Disposition'] = 'attachment; filename=graph.png'
	sensorid = int(request.GET.get('sensorid', ''))
	start = request.GET.get('start', '')
	end = request.GET.get('end', '')
	starttime = int(mktime(datetime.strptime(start,'%Y%m%d%H%M').timetuple()))
	endtime = int(mktime(datetime.strptime(end,'%Y%m%d%H%M').timetuple()))
	return get_graphimage(sensorid,starttime,endtime)

@route('/static/<filepath:path>')
def server_static(filepath):
	return static_file(filepath, root='static')

debug(True)
run(host='localhost', port=8080, reloader=True)
