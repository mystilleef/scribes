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

u"""
Command line help manual

This module contains code that generates the command line help manual.

@author: Lateef Alabi-Oki
@organiation: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""


def help():
	"""
	Generate the command line help manual.
	"""
	from internationalization import msg0124, msg0125, msg0126, msg0127, msg0128
	from internationalization import msg0129, msg0130
	print msg0124
	print
	print msg0125
	print
	print msg0126
	print
	print "\t-h, --help\t" + msg0127
	print "\t-v, --version\t" + msg0128
	print "\t-n, --newfile\t" + msg0129
	print "\t-r, --readonly\t" + msg0130
	print
	print "http://scribes.sourceforge.net/"
	return
