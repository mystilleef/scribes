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
General information about Scribes.

@author: Lateef Alabi-Oki
@organiation: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from os import environ
from dbus import SessionBus, Interface, glib
from gobject import MainLoop
mainloop = MainLoop()
session_bus = SessionBus()
dbus_proxy_obj = session_bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
dbus_iface = Interface(dbus_proxy_obj, 'org.freedesktop.DBus')
home_folder = environ["HOME"]
desktop_folder = home_folder + "/Desktop"
metadata_folder = home_folder + "/.gnome2/scribes/"
home_plugin_folder = metadata_folder + "plugins"
name = "scribes"
scribes_prefix = "/usr"
scribes_executable_path = scribes_prefix + "/bin"
scribes_executable_client = scribes_executable_path + "/.scribesclient"
scribes_executable_server = scribes_executable_path + "/scribes"
scribes_data_path = "/usr/share"
scribes_sysconfdir = "/usr/etc"
scribes_data_folder = scribes_data_path + "/scribes"
core_plugin_folder = scribes_data_folder + "/plugins"
python_path = "/usr/lib/python2.5/site-packages"
version = "0.3.2.10-rev25"
author = ["Author:", "\tLateef Alabi-Oki <mystilleef@gmail.com>\n",
			"Contributors:",
			"\tHerman Polloni <hpolloni@gmail.com>",
			"\tJames Laver <james.laver@gmail.com>",
			"\tHugo Madureira <madureira.hugo@gmail.com>",
			"\tJustin Joy <mavx21@gmail.com>",
			"\tFrank Hale <frankhale@gmail.com>",
			"\tHideo Hattori <dfgas409@kcc.zaq.ne.jp>",
			"\tMatt Murphy <matt.murphy@crmpc.com>",
			"\tChris Wagner <Chris.Wagner@softhome.net>",
			"\tShawn Bright <nephish@gmail.com>",
			"\tPeter Magnusson <peter.magnusson@crippledcanary.se>",
			"\tJakub Sadowinski <paypal@unihex.com>",
		]
documenters = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
artists = ["Alexandre Moore <alexandre.moore@gmail.com>", "Panos Laganakos <panos.laganakos@gmail.com>"]
website = "http://scribes.sourceforge.net/"
copyrights = "Copyright © 2005 Lateef Alabi-Oki"
translators = "Brazilian Portuguese translation by Leonardo F. Fontenelle \
<leo.fontenelle@gmail.com>\nRussian translation by Paul Chavard \
<polo@tchak.net>\nGerman translation by Maximilian Baumgart \
<max.baumgart@web.de>\nGerman translation by Steffen Klemer <moh@gmx.org>\nItalian translation by Stefano Esposito \
<ragnarok@email.it>\nFrench translation by Gautier Portet \
<kassoulet@gmail.com>\nDutch translation by Filip Vervloesem \
<filipvervloesem@users.sourceforge.net> \
\nSwedish translation by Daniel Nylander <po@danielnylander.se> \
\nChinese translation by chaos proton <chaos.proton@gmail.com>"
