import commands,logging

class daenetip(object):
	ip = ''
	__relayoid = '.1.3.6.1.4.1.19865.1.2.2.1.{0}'
	__tempoid  = '.1.3.6.1.4.1.19865.1.2.3.1.{0}'
	rwcommunity = 'private';
	rocommunity = '000000000000';
	appmode = 'dev' # dev / production

	def __init__(self,ip,appmode):
		self.ip = ip
		self.appmode = appmode

	def gettemp(self,sensorid):
		if self.appmode == "dev":
			return 23.3
		else:
			oid = self.__tempoid.format(sensorid)
			ret = commands.getstatusoutput('snmpget -v1 -c {2} -Ovq {0} {1}'.
							format(self.ip, oid, self.rocommunity))

			if ret[0] == 0:
				temp = 1.2 * (float(ret[1])/1024.0) * (8.0/4.7) * 100.0
				temp = round(temp,2)

				return temp
			else:
				err = 'Error reading relay data: '+ret[1]+'. Error code '+str(ret[0])
				#logging.error(err)
				raise Exception(err)

	def getrelay(self,relayid):
		if self.appmode == "dev":
			return None
		else:
			oid = self.__relayoid.format(relayid)
			ret = commands.getstatusoutput('snmpget -v1 -c {2} -Ovq {0} {1}'.
				format(self.ip, oid, self.rocommunity))

			if ret[0] == 0:
				return int(ret[1])
			else:
				err = 'Error reading relay data: '+ret[1]+'. Error code '+str(ret[0])
						#logging.error(err)
				raise Exception(err)

	def setrelay(self,relayid, state):
		if self.appmode == "dev":
			return
		else:
			if self.getrelay(relayid) == state:
				logging.debug('Relay state already set to {0}. Skipping.'.format(state))
			else:
				oid = self.__relayoid.format(relayid)
				ret = commands.getstatusoutput('snmpset -v1 -c {3} {0} {1} i {2}'.
						format(self.ip, oid, state, self.rwcommunity))

				if ret[0] != 0:
					err = 'Error writing relay data: '+ret[1]+'. Error code '+str(ret[0])
					#logging.error(err)
					raise Exception(err)
