import pynats
import time
import string 
import threading

send_cnt=0
recv_cnt=0
r_msg="0"*3900
N=800
old_cnt_sec=0
temp_cnt=0
now=0
oldtime=0
flag=0
ping_delay=0
pong_delay=0
old_sec=0
ping_delay_3sec=0
send_cnt_3sec=0

def callback(msg):
	'''global flag
	flag=1'''
	global recv_cnt,ping_delay_3sec,pong_delay
	#print msg.data[:34]
	recv_cnt+=1
	ping_delay_3sec+=(string.atof(msg.data[0:20])-string.atof(msg.data[21:41]))
	

puber=pynats.Connection(verbose=True)
puber_check=pynats.Connection(verbose=True)
puber.connect()
puber_check.connect()
puber_check.subscribe('pong.fiat',callback)

def sender():
	global old_sec,temp_cnt,old_cnt_sec,ping_delay_3sec,send_cnt_3sec,N,send_cnt,puber,r_msg
	while(1):
		sec=time.time()
		if(sec-old_sec>1):
			old_cnt_sec+=1
			temp_cnt=0
			old_sec=sec
			if(old_cnt_sec==3):
				print 'now_time: %f N: %d send: %d recv: %d ping_delay: %f' % (sec,N,send_cnt,recv_cnt,ping_delay_3sec/send_cnt_3sec)
				old_cnt_sec=0
				send_cnt_3sec=0
				ping_delay_3sec=0
		else:
			if(temp_cnt<N):
				send_cnt+=1
				temp_cnt+=1
				send_cnt_3sec+=1
				#print 'sender'
				#print '%10.9lf.%d' % (sec,N/800)
				puber.publish('ping.fiat','%10.9lf.%d%s' % (sec,N/800,r_msg))
				if(send_cnt%50000==0):
					N+=800
				#puber.wait(count=1)
			
			else:
				'noop'

def recver():
	global puber_check
	#global recv_cnt,ping_delay_3sec,pong_delay
	#print 'recver'
	puber_check.wait(count=1000000)
		
threads=[]
t1=threading.Thread(target=sender)
threads.append(t1)
t2=threading.Thread(target=recver)
threads.append(t2)

for t in threads:
	t.setDaemon(True)
	t.start()
	#print 1

t.join()
			
puber.close()
puber_check.close()

















'''
while (1):
	sec=time.time()
	now=time.time()
	oldtime=time.time()
	if(sec-old_sec>1):
		temp_cnt=0
		old_sec=sec
		old_count_sec+=1
	if(old_count_sec==3):
	    old_count_sec=0
	    print 'send: %d recv: %d' % (send_cnt,recv_cnt)
	else:
		if (temp_cnt<N):
			while (now-oldtime<1.0/N):
				now=time.time()
			oldtime=now
			puber.publish('ping.fiat',("%f" % time.time())+r_msg)
			puber.wait(count=1)
			'if (flag==0):
				puber.reconnect()
				print "reconnect1"'
			
			flag=0
			temp_cnt+=1
			send_cnt+=1
		else:
			'noop'
'''
