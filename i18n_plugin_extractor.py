#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2007 Lateef Alabi-Oki
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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

"""
This module generates a list of files that need internationalization
and writes the result to i18n_files.txt.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

def main(argv):
	from operator import ne
	if ne(argv[0], "plugins"): raise RuntimeError
	files = __get_i18n_files(argv[0])
	__write_to_file(files)
	return

def __get_i18n_files(folder):
	from os import walk
	from operator import eq
	i18n_files = []
	for root, dirs, files in walk(folder):
		for filename in files:
			if filename.endswith("glade") or eq(filename, "i18n.py"):
				_file = root + "/" + filename + "\n"
				i18n_files.append(_file)
	return i18n_files

def __write_to_file(files):
	string = "".join(files)
	handle = open("i18n_plugin_files.txt", "w")
	handle.write(string)
	handle.close()
	return

if __name__ == "__main__":
	# Initialize the program.
	from sys import argv
	main(argv[1:])
