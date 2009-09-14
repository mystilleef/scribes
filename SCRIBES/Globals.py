from os import environ
from dbus import SessionBus, Interface, glib
SCRIBES_DBUS_SERVICE = "net.sourceforge.Scribes"
SCRIBES_DBUS_PATH = "/net/sourceforge/Scribes"
SCRIBES_SAVE_PROCESS_DBUS_SERVICE = "net.sourceforge.ScribesSaveProcess"
SCRIBES_SAVE_PROCESS_DBUS_PATH = "/net/sourceforge/ScribesSaveProcess"
session_bus = SessionBus()
dbus_proxy_obj = session_bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
dbus_iface = Interface(dbus_proxy_obj, 'org.freedesktop.DBus')
home_folder = environ["HOME"]
folder_ = home_folder + "/Desktop"
from os.path import exists
desktop_folder = folder_ if exists(folder_) else home_folder
metadata_folder = home_folder + "/.gnome2/scribes/"
home_plugin_folder = metadata_folder + "plugins"
home_language_plugin_folder = metadata_folder + "LanguagePlugins"
name = "scribes"
prefix = "/usr"
executable_path = prefix + "/bin"
data_path = "/usr/share"
sysconfdir = "/usr/etc"
data_folder = data_path + "/scribes"
core_plugin_folder = data_folder + "/plugins"
core_language_plugin_folder = data_folder + "/LanguagePlugins"
python_path = "/usr/lib/python2.6/dist-packages"
version = "0.4-dev-build484"
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
