from SCRIBES.SignalConnectionManager import SignalManager

class Spooler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "new-save-job", self.__update_cb, False, True)
		self.connect(manager, "save-data", self.__update_cb, False, True)
		self.connect(manager, "finished-save-job", self.__update_cb, False, False)
		editor.register_object(self) 
		print "Initialized save job spooling object."

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from collections import deque
		self.__wait_queue = deque()
		self.__busy_queue = deque()
		self.__is_busy = False
		return False

	def __start_job(self):
		try:
			from gobject import idle_add
			job = self.__wait_queue.pop()
			self.__busy_queue.append(job)
			idle_add(self.__manager.emit, "start-save-job", job)
			print "Sending a job for saving..."
		except IndexError:
			self.__emit_is_busy(False)
		return False

	def __update(self, job, new_job):
		if new_job is True: self.__emit_is_busy(True)
		self.__wait_queue.appendleft(job) if new_job else self.__busy_queue.pop()
		if self.__busy_queue: return False 
		self.__start_job()
		# from gobject import idle_add
		# idle_add(self.__start_job)
		return False

	def __emit_is_busy(self, is_busy):
		if is_busy == self.__is_busy: return False
		self.__is_busy = is_busy
		from gobject import idle_add
		idle_add(self.__manager.emit, "saving-in-progress", is_busy)
		print "Saving in progress: ", is_busy
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		print "Destroying save job spooling instance"
		del self
		return False

	def __update_cb(self, manager, job, new_job):
		from gobject import idle_add
		idle_add(self.__update, job, new_job)
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
