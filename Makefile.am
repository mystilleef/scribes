edit = sed -e 's,@python_path\@,$(pythondir),g'
startupdir = $(prefix)/bin
startup_script = scribes
startup_script_in_files = $(startup_script).in
startup_DATA = $(startup_script_in_files:.in=)

$(startup_script): Makefile $(startup_script_in_files)
	rm -f $(startup_script) $(startup_script).tmp
	$(edit) $(startup_script_in_files) > $(startup_script).tmp
	mv $(startup_script).tmp $(startup_script)

ACLOCAL_AMFLAGS = -I m4

SUBDIRS = po help data SCRIBES

# Workaround broken scrollkeeper that doesn't remove its files on
# uninstall.
distuninstallcheck_listfiles = find . -type f -print | grep -v scrollkeeper

DISTCHECK_CONFIGURE_FLAGS =	\
	--disable-scrollkeeper

EXTRA_DIST = m4 \
	autogen.sh \
	depcheck.py \
	$(startup_script_in_files) \
	xmldocs.make \
	omf.make \
	gnome-doc-utils.make \
	intltool-merge.in \
	intltool-update.in \
	intltool-extract.in \
	i18n_plugin_extractor.py \
	CONTRIBUTORS \
	TODO \
	plugins \
	compile.py \
	TRANSLATORS

DISTCLEANFILES = \
	$(startup_script) \
	gnome-doc-utils.make

install-data-hook:
	echo "Start byte compiling plugins..."
	python -OO compile.py
	echo "Finished byte compiling plugins"
	if [ -d $(DESTDIR)$(datadir)/scribes/plugins ]; then \
		echo "removing " $(DESTDIR)$(datadir)/scribes/plugins ;\
		rm -rf $(DESTDIR)$(datadir)/scribes/plugins ;\
		echo "removed " $(DESTDIR)$(datadir)/scribes/plugins ;\
	fi
	cp -R plugins $(DESTDIR)$(datadir)/scribes
	chmod 755 $(DESTDIR)$(startupdir)/$(startup_script)
