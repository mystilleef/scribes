# -*- coding: utf-8 -*-
# Copyright (C) 2005 Lateef Alabi-Oki
#
# This file is part of Scribes.
#
# Scribes is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Scribes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Scribes; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
This module exposes a class that is responsible for processing the text
editor's command line options and arguments.

@author: Lateef Alabi-Oki
@organiation: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class CommandLineProcessor(object):
	"""
	This class instantiates an object that is responsible for processing the
	text editor's command line options and arguments. The text editor currently
	supports four options, -h (--help), -v(--version), -n(--new) and
	-r(--readonly). Arguments are any valid file name or URI. If arguments are
	file names, they are converted to URIs before being further processed.
	"""

	def __init__(self, argv):
		self._init_attributes(argv)
		self._process_options()
		self._process_arguments()

	def _init_attributes(self, argv):
		# True when -n, or --new, is passed as an option to the text editor.
		self.newfile_flag = False

		# True when -r, or --readonly, is passed as an option to the text
		# editor.
		self.readonly_flag = False

		# True when to trigger premature termination of the text editor.
		self.exit_flag = False

		# Command line options supported by the text editor.
		self.options = ["-n", "--newfile", "-r", "--readonly", "-v",
						"--version", "-h", "--help", "-i", "--info"]

		# The preferred encoding of the host system.
		from locale import getpreferredencoding
		self.encoding = getpreferredencoding(True)

		# List of options retreived from the command line.
		self.option_list = []

		# List of arguments, or file names(uris), retreived from the command
		# line.
		self.argument_list = []

		# List of valid URIs
		self.uri_list = []

		# Options and arguments from the command line.
		self.argv = argv
		return

	def _process_options(self):
		self.option_list = self._get_command_line_options()
		if self.option_list:
			# Options were detected.
			self.option_list = self._validate_command_line_options()
			if self.option_list:
				# Validation is successful.
				self._process_command_line_options()
			else:
				# An invalid option exists. The editor should not be launched
				# and the CommandLineProcessor instance should be destroyed.
				self.exit_flag = True
				self._clean_up()
		return

	def _process_arguments(self):
		self.argument_list = self._get_command_line_arguments()
		if self.argument_list:
			self.uri_list = self._convert_arguments_to_uris()
			if not self.uri_list:
				self.exit_flag = True
				self._clean_up()
		else:
			print self.option_list[0], "takes one or more arguments"
			from internationalization import msg0039
			print msg0039.decode("utf-8").encode(self.encoding)
			self.exit_flag = True
			self._clean_up()
		return

	def _get_command_line_options(self):
		option_list = []
		for options in self.argv:
			if options.startswith("-"):
				option_list.append(options)
		return option_list

	def _validate_command_line_options(self):
		if len(self.option_list) > 1:
			# Show an error message when more than one option is passed to the
			# text editor as arguments.
			self.exit_flag = True
			option_list = []
			from internationalization import msg0040, msg0039
			print msg0040.decode("utf-8").encode(self.encoding)
			print msg0039.decode("utf-8").encode(self.encoding)
		else:
			option = self.option_list[0]
			if option in self.options:
				option_list = self.option_list
			else:
				# Show an error message when an invalid option is passed to the
				# text editor as an argument.
				self.exit_flag = True
				option_list = []
				from internationalization import msg0038, msg0039
				print msg0038.decode("utf-8").encode(self.encoding) % option
				print msg0039.decode("utf-8").encode(self.encoding)
		return option_list

	def _process_command_line_options(self):
		option = self.option_list[0]
		if option in ("-h", "--help"):
			from usage import help as chelp
			chelp()
			self.exit_flag = True
			self._clean_up()
		if option in ("-i", "--info"):
			self.__print_info()
			self.exit_flag = True
			self._clean_up()
		elif option in ("-v", "--version"):
			from info import version
			from internationalization import msg0042
			print msg0042.decode("utf-8").encode(self.encoding) % \
			version.encode(self.encoding, "replace")
			self.exit_flag = True
			self._clean_up()
		elif option in ("-n", "--newfile"):
			self.newfile_flag = True
		elif option in ("-r", "--readonly"):
			self.readonly_flag = True
		return

	def _get_command_line_arguments(self):
		# Filter options from the command line argument list.
		argument_list = [args for args in self.argv if not args.startswith("-")]
		return argument_list

	def _convert_arguments_to_uris(self):
		from gnomevfs import make_uri_from_shell_arg, exists, URI
		uri_list = []
		for files in self.argument_list:
			file_uri = make_uri_from_shell_arg(files.strip())
			uri = URI(file_uri)
			if uri.is_local or str(uri).startswith("file:///"):
				if exists(file_uri):
					uri_list.append(file_uri)
				else:
					if self.newfile_flag:
						# Create a new file if one does not exist.
						result = self._create_new_uri(file_uri)
						if result:
							uri_list.append(file_uri)
					else:
						# URI does not exist
						from internationalization import msg0043
						print msg0043.decode(u"utf-8").encode(self.encoding) % files
			else:
				try:
					from gnomevfs import AccessDeniedError, NotFoundError
					from gnomevfs import get_file_info
					get_file_info(file_uri)
					uri_list.append(file_uri)
				except AccessDeniedError:
					uri_list.append(file_uri)
				except NotFoundError:
					if self.newfile_flag:
						# Create a new file if one does not exist.
						result = self._create_new_uri(file_uri)
						if result:
							uri_list.append(file_uri)
					else:
						# URI does not exist
						from internationalization import msg0043
						print msg0043.decode(u"utf-8").encode(self.encoding) % files
				except:
					# Cannot determine
					print "Invalid file Error, line 312, commandline.py."
					uri_list.append(file_uri)
		return uri_list

	def _create_new_uri(self, file_uri):
		value = True
		from gnomevfs import create, OPEN_WRITE
		try:
			create(file_uri, OPEN_WRITE)
		except:
			value = False
			from gnomevfs import URI
			uri_object = URI(file_uri)
			print "You do not have permissions to create", uri_object.path
		return value

	def __print_info(self):
		print "========================================================"
		import os
		print "System Info: ", os.uname()
		import sys
		print "Python Version: ", sys.version
		print "System Byteorder: ", sys.byteorder
		print "Python Modules: ", sys.builtin_module_names
		print "========================================================"
		from info import version
		print "Scribes Version: ", version
		import dbus
		print "Dbus Version: ", dbus.version
		import gtk
		print "GTK+ Version: ", gtk.gtk_version
		import gtk
		print "PyGTK Version: ",	gtk.pygtk_version
		import gnome
		print "GNOME Python Version: ", gnome.gnome_python_version
		try:
			import psyco
			print "Psyco Version: ", psyco.version_info
		except ImportError:
			print "Psyco Not Installed"
		print "========================================================"
		from SCRIBES.info import dbus_iface
		services = dbus_iface.ListNames()
		service = "net.sourceforge.Scribes"
		print "Running Instance: ", services.count(service)
		print "========================================================"
		from SCRIBES.info import scribes_executable_path
		from SCRIBES.info import python_path, core_plugin_folder
		from SCRIBES.info import scribes_data_folder
		print "Python Path: ", python_path
		print "Plugin Path: ", core_plugin_folder
		print "Data Path: ", scribes_data_folder
		print "Executable Path: ", scribes_executable_path
		print "========================================================"
		return

	def _clean_up(self):
		if self.exit_flag: raise SystemExit
		from gc import collect
		del self
		collect()
		return
