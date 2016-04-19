import pynats
import string
import time
send_cnt=0
recv_cnt=0
flag=0
ping_delay=0.0
N=0
recv_cnt3=0

suber=pynats.Connection(verbose=True)
suber.connect()
suber_pong=pynats.Connection(verbose=True)
suber_pong.connect()
start=time.clock();


def callback(msg):
	global send_cnt
	global recv_cnt
	global flag
	global N
	global ping_delay
	global recv_cnt3
	flag=1
	send_cnt+=1
	recv_cnt+=1
	recv_cnt3+=1
	now=time.time()
	N=800*string.atoi(msg.data[21])
	stri=' %s'%(msg.data[22:1007])
	#print msg.data[:30]
	stri1='%s' %(msg.data[0:20])
	ping_delay+=now-string.atof(stri1)
	suber_pong.publish('pong.fiat','%10.9lf.%s.' % (now,msg.data[:20])+stri)
	
			
	


suber.subscribe('ping.fiat',callback)

flag=0

old_sec=time.time()
old_cnt_sec=0
now=0
while(1):
	suber.wait(count=1)
	now=time.time()
	if(now-old_sec>3):
		old_sec=now
		print '%10.9lf N: %d  send: %d  recv : %d  ping_delay: %f' % (now,N,send_cnt,recv_cnt,ping_delay/recv_cnt3)
		ping_delay=0.0
		recv_cnt3=0
	'''
	if(flag==0):
		suber.reconnect()
		print "connect2"'''
	
	flag=0


suber.close()
