#! /usr/bin/env python
# -*- coding: utf8 -*-

def check_dependencies():
	try:
		# Check for D-Bus Python Bindings.
		try:
			import dbus
			if dbus.version < (0, 70, 0): raise AssertionError
			print "Checking for D-Bus (Python Bindings)... yes"
		except ImportError:
			print "Error: Python bindings for D-Bus was not found."
			raise SystemExit
		except AssertionError:
			print "Error: Version 0.70 or better of dbus-python needed."
			raise SystemExit
		# Check for PyGTK.
		try:
			import gtk
			if gtk.pygtk_version < (2, 10, 0): raise AssertionError
			print "Checking for PyGTK... yes"
		except ImportError:
			print "Error: PyGTK was not found."
			raise SystemExit
		except AssertionError:
			print "Error: Version 2.10.0 or better of PyGTK needed."
			raise SystemExit
		# Check for pygtksourceview2.
		try:
			import gtksourceview2
			print gtksourceview2
			print "Checking for pygtksourceview2... yes"
		except ImportError:
			print "Error: pygtksourceview2 was not found."
			raise SystemExit
		try:
			import gtkspell
			print gtkspell
			print "Checking for gtkspell-python... yes"
		except ImportError:
			print "Error: Python bindings for gtkspell was not found."
			raise SystemExit
	except SystemExit:
		from sys import exit
		exit(1)
	return

check_dependencies()
