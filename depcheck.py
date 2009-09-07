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
		# Check for Pygobject.
		try:
			import gobject
			print "Checking for Pygobject... yes"
		except ImportError:
			print "Error: pygobject was not found."
			raise SystemExit
		# Check for GTK.
		try:
			import gtk
			if gtk.gtk_version < (2, 10, 0): raise AssertionError
			print "Checking for GTK... yes"
		except ImportError:
			print "Error: GTK was not found."
			raise SystemExit
		except AssertionError:
			print "Error: Version 2.10.0 or better of GTK needed."
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
		# Check for GNOME Python.
		try:
			import gnome
			if gnome.gnome_python_version < (2, 12, 0): raise AssertionError
			print "Checking for GNOME Python... yes"
		except ImportError:
			print "Error: gnome-python was not found."
			raise SystemExit
		except AssertionError:
			print "Error: Version 2.12.0 or better of gnome-python needed."
			raise SystemExit
		# Check for GNOME Python Desktop.
		try:
			import gtksourceview
			print "Checking for GNOME Python Desktop... yes"
		except ImportError:
			print "Error: gnome-python-desktop was not found."
			raise SystemExit
		# Check for GNOME Python Extras.
		try:
			import gtkspell
			print "Checking for GNOME Python Extras... yes"
		except ImportError:
			print "Error: gnome-python-extras was not found."
			raise SystemExit
	except SystemExit:
		from sys import exit
		exit(1)
	return

check_dependencies()
