edit = sed \
	-e 's,@pixmapsdir\@,$(pixmapsdir),g' \
	-e 's,@icondir\@,$(icondir),g' \
	-e 's,@svgicondir\@, $(svgicondir),g' \
	-e 's,@scribes_prefix\@,$(prefix),g' \
	-e 's,@scribes_data_path\@,$(datadir),g' \
	-e 's,@VERSION\@,$(VERSION),g'

# Process Scribes logo.
pixmapsdir = $(datadir)/pixmaps
pixmaps_DATA = scribes.svg

# Process Scribes data files.
scribesdir = $(datadir)/scribes
scribes_DATA = Editor.glade \
	bookmarks.png \
	ModificationDialog.glade \
	EncodingSelectionWindow.glade \
	EncodingErrorWindow.glade \
	MessageWindow.glade \
	throbber-active.gif \
	throbber-inactive.png

# icondir = $(datadir)/icons/hicolor/48x48/apps
# icon_DATA = scribes.png
# svgicondir = $(datadir)/icons/hicolor/scalable/apps
# svgicon_DATA = scribes.svg

icondir = $(datadir)/icons/hicolor/scalable/apps
icon_DATA = scribes.svg

gtk_update_icon_cache = gtk-update-icon-cache -f -t $(datadir)/icons/hicolor
install-data-hook:
		@-if test -z "$(DESTDIR)"; then \
				echo "Updating Gtk icon cache."; \
				$(gtk_update_icon_cache); \
		else \
				echo "*** Icon cache not updated.  After install, run this:"; \
				echo "***   $(gtk_update_icon_cache)"; \
		fi

# Process Scribes freedesktop.org metadata for GNOME.
Desktopdir = $(datadir)/applications
Desktop_files = scribes.desktop
Desktop_in_files = scribes.desktop.in
Desktop_DATA = $(Desktop_in_files:.desktop.in=.desktop)
@INTLTOOL_DESKTOP_RULE@

EXTRA_DIST = bookmarks.png \
	throbber-inactive.png \
	throbber-active.gif \
	scribes.desktop.in \
	ModificationDialog.glade \
	EncodingSelectionWindow.glade \
	EncodingErrorWindow.glade \
	Editor.glade \
	MessageWindow.glade \
	scribes.svg

CLEANFILES = $(Desktop_DATA)
