from ScribesPylint.checkers import BaseRawChecker
from ScribesPylint.interfaces import ILinter, IRawChecker
from ScribesPylint.utils import MessagesHandlerMixIn, ReportsHandlerMixIn
#from poo import *

class Linter(MessagesHandlerMixIn, ReportsHandlerMixIn, BaseRawChecker):

	__implements__ = (ILinter, IRawChecker)

	name = 'master'
	priority = 0
	level = 0
	msgs = {}
	may_be_disabled = False

	def __init__(self):
		# init options
		# visit variables
		from ScribesPylint.reporters.text import ParseableTextReporter
		self.reporter = ParseableTextReporter()
		self.base_name = None
		self.base_file = None
		self.current_name = None
		self.current_file = None
		self.stats = None
		self.__checkers = []
		MessagesHandlerMixIn.__init__(self)
		ReportsHandlerMixIn.__init__(self)
		BaseRawChecker.__init__(self)
		self.register_checker(self)
		self.__register_checkers()
		self.set_reporter(self.reporter)
		# Error messages to ignore due to unreliability.
		self.reporter.ignore = ("E1103", "E0611", "E1101") #("E0611", "E1101", "E0203")
		# Warning or error messages to reveal.
		self.reporter.reveal = (
			"W0101", "W0102", "W0104", "W0107", "W0211", "W0231", "W0233", "W0301", "W0311",
			"W0331", "W0333", "W0404", "W0406", "W0410", "W0601", "W0602", "W0604", "C0121",
			"C0202", "C0203", "C0322", "C0323", "C0324", "R0801", "W1111"
		)

	def check(self, filename, modification_time):
		from Utils import update_python_environment_with
		update_python_environment_with(filename)
		self.reporter.error_messages = []
		from os.path import basename, dirname
		module = basename(filename).strip(".py")
		self.current_name = module
		self.current_file = filename
		self.base_file = dirname(filename)
		self.base_name = basename(self.base_file)
		rawcheckers = []
		from ScribesPylint.utils import PyLintASTWalker
		walker = PyLintASTWalker()
		from ScribesPylint.logilab.common.interface import implements
		from ScribesPylint.interfaces import IASTNGChecker
		for checker in self.sort_checkers():
			checker.open()
			if implements(checker, IASTNGChecker):
				walker.add_checker(checker)
			if implements(checker, IRawChecker) and checker is not self: #XXX
				rawcheckers.append(checker)
		self.set_current_module(module, filename)
		astng = self.get_astng(filename, module, modification_time)
		messages = self.check_astng_module(astng, walker, rawcheckers)
		del astng
		del walker
		self.set_current_module("")
		self.__checkers.reverse()
		for checker in self.__checkers:
			checker.close()
		return messages

	def get_astng(self, filepath, modname, modification_time):
		"""return a astng representation for a module"""
		try:
			from ScribesPylint.logilab.astng.manager import ASTNGManager
			manager = ASTNGManager(borg=False)
			manager.brain = {}
			manager.reset_cache()
			manager.brain = {}
			from Utils import file_has_changed
			if file_has_changed(filepath, modification_time): return None
			astng = manager.astng_from_file(filepath)
		except (SyntaxError, IndentationError):
			return None
		except Exception:
			return None
		return astng

	def check_astng_module(self, astng, walker, rawcheckers):
		if astng is None: return None
		from ScribesPylint.logilab.common.fileutils import norm_open
		stream = norm_open(astng.file)
		for checker in rawcheckers:
			stream.seek(0)
			checker.process_module(stream)
		walker.walk(astng)
		return self.reporter.error_messages

	def __register_checkers(self):
		from ScribesPylint.checkers.base import register
		register(self)
		from ScribesPylint.checkers.classes import register
		register(self)
		from ScribesPylint.checkers.exceptions import register
		register(self)
		from ScribesPylint.checkers.format import register
		register(self)
		from ScribesPylint.checkers.imports import register
		register(self)
		from ScribesPylint.checkers.newstyle import register
		register(self)
		from ScribesPylint.checkers.string_format import register
		register(self)
		from ScribesPylint.checkers.typecheck import register
		register(self)
		from ScribesPylint.checkers.variables import register
		register(self)
		return False

	def sort_checkers(self, checkers=None):
		if checkers is None:
			checkers = self.__checkers
		graph = {}
		cls_instance = {}
		for checker in checkers:
			graph[checker.__class__] = set(checker.needs_checkers)
			cls_instance[checker.__class__] = checker
		from ScribesPylint.logilab.common.graph import ordered_nodes
		checkers = [cls_instance.get(cls) for cls in ordered_nodes(graph)]
		checkers.remove(self)
		checkers.insert(0, self)
		return checkers

	def set_reporter(self, reporter):
		"""set the reporter used to display messages and reports"""
		self.reporter = reporter
		reporter.linter = self

	def open(self):
		"""initialize counters"""
		self.stats = {'by_module' : {}, 'by_msg' : {},}
		from ScribesPylint.utils import MSG_TYPES
		for msg_cat in MSG_TYPES.values():
			self.stats[msg_cat] = 0

	def register_checker(self, checker):
		self.__checkers.append(checker)
		if hasattr(checker, 'reports'):
			for r_id, r_title, r_cb in checker.reports:
				self.register_report(r_id, r_title, r_cb, checker)
		if hasattr(checker, 'msgs'):
			self.register_messages(checker)
		checker.load_defaults()

	def set_current_module(self, modname, filepath=None):
		"""set the name of the currently analyzed module and
		init statistics for it
		"""
		if not modname and filepath is None: return
		self.current_name = modname
		self.current_file = filepath or modname
		self.stats['by_module'][modname] = {}
		self.stats['by_module'][modname]['statement'] = 0
		from ScribesPylint.utils import MSG_TYPES
		for msg_cat in MSG_TYPES.values():
			self.stats['by_module'][modname][msg_cat] = 0
#		 XXX hack, to be correct we need to keep module_msgs_state
#		 for every analyzed module (the problem stands with localized
#		 messages which are only detected in the .close step)
		if modname:
			self._module_msgs_state = {}
			self._module_msg_cats_state = {}

	def _get_checkers(self):
		# compute checkers needed according to activated messages and reports
		neededcheckers = set()
		for checker in self.__checkers:
			for msgid in checker.msgs:
				if self._msgs_state.get(msgid, True):
					neededcheckers.add(checker)
					break
			else:
				for reportid, _, _ in checker.reports:
					if self.is_report_enabled(reportid):
						neededcheckers.add(checker)
						break
		return self.sort_checkers(neededcheckers)
