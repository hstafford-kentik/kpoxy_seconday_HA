# unsupported
kproxy-check is a python script meant to be run as a service or background processs which will make a health check against a primary kproxy server.  It uses the telnet health check on the default port of 9996, and only checks that a response is made.   This port is configurable via command line, and must be included.

If the primay server does not respond, it will start a local kproxy daemon, which MUST be installed and preconfigured.  

The script kpoxy-check.py may be placed anywhere, but the location must be added to the kproxy-HA.service file if running as a service.

kproxy-HA.service should be placed in /etc/systemd/system/ in order to run as a service on ubuntu/debian.

kproxy-HA.service will pull configuration values from /etc/default/kentik.env which is created and used by the kproxy service.

kentik.env should replace the one found in /etc/default/kentik.env.  Again, this is only requred if running as a system daemon.

On ubuntu/debian, to install the service:
use sudo to place and edit the files as mentioned above
sudo systemctl daemon-reload
sudo systemctl enable kproxy-HA.service
sudo systemctl start kproxy-HA.service

by default, a log minimal log file will be written to /var/log/remote_kproxy_status.log

To run/test the script manually:
/usr/bin/python3 <path to script>/kproxy-check.py <IP OF PRIMARY> <HEALTHCHECK PORT> <HEALTHCHECK INTERVAL IN SECONDS> <NO. OF FAILS BEFORE STARTING LOCAL KPROXY>
