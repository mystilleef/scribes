from Globals import data_folder, metadata_folder, home_folder, desktop_folder
from Globals import session_bus, core_plugin_folder, home_plugin_folder
from Globals import home_language_plugin_folder, core_language_plugin_folder
from Globals import version, author, documenters, artists, website
from Globals import copyrights, translators, python_path, dbus_iface
from License import license_string
from gio import File
from DialogFilters import create_filter_list
from gtksourceview2 import language_manager_get_default
from EncodingGuessListMetadata import get_value as get_encoding_guess_list
from EncodedFilesMetadata import get_value as get_encoding
from EncodingMetadata import get_value as get_encoding_list
from Utils import get_language, word_pattern
from SupportedEncodings import get_supported_encodings
from gettext import gettext as _
