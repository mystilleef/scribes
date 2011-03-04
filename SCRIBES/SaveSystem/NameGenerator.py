from string import punctuation, whitespace
from SCRIBES.SignalConnectionManager import SignalManager

STRIP_CHARACTERS = punctuation + whitespace
RESERVED_CHARACTERS = ["/", "\\", "?", "%", "*", ":", "|", '"', "<", ">", ".", "&", ",", "\t"]
NUMBER_OF_WORDS = 10
NUMBER_OF_CHARACTERS = 80

class Generator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__destroy_cb)
		self.connect(manager, "generate-name", self.__generate_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__optimize, priority=PRIORITY_LOW)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __generate(self, data):
		try:
			# Get first valid line in buffer. Strip characters, mostly
			# punctuation characters, that can cause invalid Unix filenames.
			line = self.__editor.text.strip(STRIP_CHARACTERS).splitlines()[0].strip(STRIP_CHARACTERS)
			# Replace invalid characters with spaces.
			invalid_characters = [character for character in line if character in RESERVED_CHARACTERS]
			for character in invalid_characters: line = line.replace(character, " ")
			# Select first ten words and remove extras spaces to get filename
			filename = " ".join(line.split()[:NUMBER_OF_WORDS]).strip()[:NUMBER_OF_CHARACTERS].strip()
		except IndexError:
			filename = ""
		finally:
			from gobject import idle_add
			idle_add(self.__manager.emit, "newname", (filename, data))
		return False

	def __generate_on_idle(self, data):
		from gobject import idle_add, PRIORITY_LOW
		self.__timer2 = idle_add(self.__generate, data, priority=PRIORITY_LOW)
		return False

	def __remove_timer(self, _timer=1):
		try:
			timers = {
				1: self.__timer1,
				2: self.__timer2,
			}
			from gobject import source_remove
			source_remove(timers[_timer])
		except AttributeError:
			pass
		return False

	def __remove_all_timers(self):
		[self.__remove_timer(_timer) for _timer in xrange(1, 3)]
		return False

	def __optimize(self):
		self.__editor.optimize((self.__generate,))
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __destroy_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __generate_cb(self, manager, data):
		self.__remove_all_timers()
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer1 = timeout_add(1000, self.__generate_on_idle, data, priority=PRIORITY_LOW)
		return False
