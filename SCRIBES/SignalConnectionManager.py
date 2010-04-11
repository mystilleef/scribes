class SignalManager(object):

	def __init__(self):
		self.__signals = []

	def connect(self, gobject, signal_name, callback, after=False):
		connect = gobject.connect if not after else gobject.connect_after
		signal_id = gobject.connect(signal_name, callback)
		self.__signals.append((gobject, signal_id))
		return signal_id

	def disconnect(self):
		__disconnect = lambda gobject, signal_id: gobject.disconnect(signal_id) if gobject.handler_is_connected(signal_id) else None
		[__disconnect(gobject, signal_id) for gobject, signal_id in self.__signals]
		return
