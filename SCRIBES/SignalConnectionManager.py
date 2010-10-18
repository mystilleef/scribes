class SignalManager(object):

	def __init__(self, editor=None):
		if editor: editor.response()
		self.__signals = []
		if editor: editor.response()
		self.__editor = editor

	def connect(self, gobject, signal_name, callback, after=False):
		if self.__editor: self.__editor.response()
		connect = gobject.connect if after is False else gobject.connect_after
		signal_id = connect(signal_name, callback)
		self.__signals.append((gobject, signal_id))
		if self.__editor: self.__editor.response()
		return signal_id

	def disconnect(self):
		__disconnect = self.__disconnect
		[__disconnect(gobject, signal_id) for gobject, signal_id in self.__signals]
		return

	def __disconnect(self, gobject, signal_id):
		if self.__editor: self.__editor.response()
		if not gobject.handler_is_connected(signal_id): return False
		gobject.disconnect(signal_id)
		if self.__editor: self.__editor.response()
		return False
