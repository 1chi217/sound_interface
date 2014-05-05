#!/usr/bin/env python

import sys
import rospy
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String
from std_srvs.srv import Empty

soundhandle = SoundClient()

def callService(service):
	call = rospy.ServiceProxy(service, Empty) 
	try:
		call()
		return 0         
	except rospy.ServiceException, e:
		rospy.logwarn("Service call failed: %s",e)
		return 1

def callback(data):
	
	rospy.loginfo("%s",data.data)
	voice = 'voice_kal_diphone'
	s = ' '    

	if data.data == 'pioneer, follow me.':
		s = 'I will follow you.'
		if callService('/tracking/start_tracking'):
			s = 'Service call failed'

	if data.data == 'pioneer, halt.':
		s = 'Ok, I halt.'
		if callService('/tracking/stop_tracking'):
			s = 'Service call failed'

	if data.data == 'pioneer, stop.':
		s = 'Ok, I stop.'
		if callService('/tracking/stop_tracking'):
			s = 'Service call failed'

	if data.data == 'Emergency stop':
		s = 'Emergency stop' 
		if callService('/RosAria/disable_motors'):
			s = 'Service call failed'
    
	if s != ' ':
		soundhandle.say(s,voice)

if __name__ == '__main__':
    
    rospy.init_node('sound_interface', anonymous = True)
    rospy.Subscriber('/recognizer/output', String, callback)

    rospy.spin()

    
   
            
