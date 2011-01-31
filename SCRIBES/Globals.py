# -*- coding: utf-8 -*-
from os import environ
from os.path import join, expanduser
from dbus import SessionBus, Interface, glib
from xdg.BaseDirectory import xdg_config_home, xdg_data_home
SCRIBES_DBUS_SERVICE = "net.sourceforge.Scribes"
SCRIBES_DBUS_PATH = "/net/sourceforge/Scribes"
SCRIBES_SAVE_PROCESS_DBUS_SERVICE = "net.sourceforge.ScribesSaveProcess"
SCRIBES_SAVE_PROCESS_DBUS_PATH = "/net/sourceforge/ScribesSaveProcess"
session_bus = SessionBus()
dbus_proxy_obj = session_bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
dbus_iface = Interface(dbus_proxy_obj, 'org.freedesktop.DBus')
home_folder = expanduser("~")
from tempfile import gettempdir
tmp_folder = gettempdir()
folder_ = join(home_folder, "Desktop")
from os.path import exists
desktop_folder = folder_ if exists(folder_) else home_folder
metadata_folder = config_folder = join(xdg_config_home, "scribes")
print_settings_filename = join(metadata_folder, "ScribesPrintSettings.txt")
home_plugin_folder = home_generic_plugin_folder = join(config_folder, "GenericPlugins")
home_language_plugin_folder = join(config_folder, "LanguagePlugins")
scribes_theme_folder = join(config_folder, "styles")
storage_folder = join(config_folder, ".config")
default_home_theme_folder = join(xdg_data_home, "gtksourceview-2.0", "styles")
name = "scribes"
prefix = "/usr"
executable_path = join(prefix, "bin")
data_path = "/usr/share"
library_path = "/usr/lib"
sysconfdir = "/usr/etc"
data_folder = join(data_path, "scribes")
root_plugin_folder = join(library_path, "scribes")
core_plugin_folder = core_generic_plugin_folder = join(root_plugin_folder, "GenericPlugins")
core_language_plugin_folder = join(root_plugin_folder, "LanguagePlugins")
python_path = "/usr/lib/python2.6/dist-packages"
version = "0.4-dev-build817"
author = ["Author:", "\tLateef Alabi-Oki <mystilleef@gmail.com>\n",
			"Contributors:",
			"\tIb Lundgren <ib.lundgren@gmail.com>",
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
			"\tRockallite Wulf <rockalite@users.sourceforge.net>",
			"\tJavier Lorenzana <skaiuoquer@gmail.com>",
			"\tKuba <kubasado@gmail.com>",
		]
documenters = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
artists = ["Alexandre Moore <alexandre.moore@gmail.com>", "Panos Laganakos <panos.laganakos@gmail.com>"]
website = "http://scribes.sf.net/"
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
