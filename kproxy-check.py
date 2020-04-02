import time
import telnetlib
import sys
import subprocess
from pathlib import Path
from datetime import datetime

subprocess.run(['systemctl', 'stop', 'kproxy.service']) # stop the local proxy, just in case.
localKproxyRunning = False
remoteError = False


primaryKproxyHost = sys.argv[1]
port = int(sys.argv[2])
remoteCheckInterval = int(sys.argv[3])
maxErrorCount = int(sys.argv[4])


logFile = '/var/log/remote_kproxy_status.log'
mainLogFile = open(logFile, 'a')
timeout = 5
firstRun = True

Path(logFile).touch()
errorCount = 0
		

while True:	
	try:
		connection = telnetlib.Telnet(primaryKproxyHost, port, timeout)
		returnData = str(connection.read_all())
		connection.close()
	except:
		returnData = 'error'
	now = datetime.now()
	#print (now.strftime("%d/%m/%Y %H:%M:%S"))
	#print (returnData)
	#print ()
	if returnData == 'error':
		remoteError = True
		if errorCount <= maxErrorCount:
			#mainLogFile.write (now.strftime("%d/%m/%Y %H:%M:%S")+' The primay kproxy did not respond to health check.')
			mainLogFile.write(now.strftime("%d/%m/%Y %H:%M:%S")+' The primay kproxy did not respond to health check.\n')
		errorCount += 1
	elif returnData.find('Connected') < 0:
		if errorCount <= maxErrorCount:
			mainLogFile.write (now.strftime("%d/%m/%Y %H:%M:%S")+' The primary kproxy responded but with bad data.\n')
		remoteError = True
		errorCount += 1
	else:
		remoteError = False
		errorCount = 0
		if firstRun == True:
			firstRun = False
			mainLogFile.write(now.strftime("%d/%m/%Y %H:%M:%S")+' Everything looks good on the primary kproxy\n')
		
	if errorCount >= maxErrorCount and localKproxyRunning == False:
		mainLogFile.write (now.strftime("%d/%m/%Y %H:%M:%S")+' Something is wrong at the remote kproxy.  Starting local kproxy service.\n')
		subprocess.run(['systemctl', 'start', 'kproxy.service'])
		mainLogFile.write (now.strftime("%d/%m/%Y %H:%M:%S")+' Local kproxy started\n')
		localKproxyRunning = True
	
	if errorCount == 0 and localKproxyRunning == True:
		mainLogFile.write (now.strftime("%d/%m/%Y %H:%M:%S")+' Looks like the primary is working normally.  Stopping local kproxy.\n')
		subprocess.run(['systemctl', 'stop', 'kproxy.service'])
		mainLogFile.write (now.strftime("%d/%m/%Y %H:%M:%S")+' Local kproxy stopped\n')
		localKproxyRunning = False
	mainLogFile.flush()
	time.sleep(remoteCheckInterval)