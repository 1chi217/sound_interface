#!/usr/bin/python

import threading
import sys
import dbus
import gobject
from dbus.mainloop.glib import DBusGMainLoop

import roslib
import rospy
from std_msgs.msg import String


class ButtonThread(threading.Thread):
	def __init__(self, DEV_ID, pub):
		# init thread
		threading.Thread.__init__(self)
		DBusGMainLoop( set_as_default=True )
		self._main_loop = gobject.MainLoop()
		self._bus = dbus.SystemBus()
		self._pub = pub

		# Figure out the path to the headset
		man = self._bus.get_object('org.bluez', '/')
		iface = dbus.Interface(man, 'org.bluez.Manager')
		adapterPath = iface.DefaultAdapter()
		print adapterPath

		self._headset = self._bus.get_object('org.bluez', adapterPath + '/dev_' + DEV_ID)
		self._headset_iface = dbus.Interface(self._headset, dbus_interface='org.bluez.Headset')
		self._headset_iface.connect_to_signal("AnswerRequested", self.on_button_pressed, sender_keyword='sender')
		
		gobject.threads_init()


	def __del__(self):
		if not self._group is None:
			self._group.Free()

	def run(self):
		try:
			self._main_loop.run()
		except KeyboardInterrupt or ROSInterruptException:
			pass

	def stop(self):
		self._main_loop.quit()
		del(self)
	
	def on_button_pressed (self, sender=None):
		self._pub.publish("Emergency stop")

if __name__ == '__main__':
	rospy.init_node('sound_interface', anonymous = True)
	pub = rospy.Publisher('/recognizer/output', String)
	mac = rospy.get_param('~MAC','ABCD');
	button = ButtonThread(mac, pub)

	button.start()
	while not rospy.is_shutdown():
		i = 1
	rospy.spin()
	button.stop()

