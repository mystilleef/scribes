class Monitor(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		from SCRIBES.Globals import session_bus
		session_bus.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0='net.sourceforge.Scribes')

	def __init_attributes(self, manager):
		self.__manager = manager
		return

	def __name_change_cb(self, *args):
		self.__manager.quit()
		return False
