edit = sed \
	-e 's,@pixmapsdir\@,$(pixmapsdir),g' \
	-e 's,@scribes_prefix\@,$(prefix),g' \
	-e 's,@scribes_lib_path\@,$(libdir),g' \
	-e 's,@scribes_data_path\@,$(datadir),g' \
	-e 's,@scribes_sysconfdir\@,$(sysconfdir),g' \
	-e 's,@python_path\@,$(pythondir),g' \
	-e 's,@VERSION\@,$(VERSION),g'

# dnl Generate "Globals.py" from "Globals.py.in."
python_files = Globals.py
python_in_files = $(python_files).in
scribesdir = $(pythondir)/SCRIBES

$(python_files): Makefile $(python_in_files)
	rm -f $(python_files) $(python_files).tmp
	$(edit) $(python_in_files) > $(python_files).tmp
	mv $(python_files).tmp $(python_files)
	if [ -d $(scribesdir) ]; then \
		echo "removing " $(scribesdir) ;\
		rm -rf $(scribesdir) ;\
		echo "removed " $(scribesdir) ;\
	fi

SUBDIRS = . GUI URILoader EncodingSystem SaveSystem SaveProcessInitializer TriggerSystem PluginInitializer

scribes_PYTHON = \
	Globals.py \
	__init__.py \
	BarObjectManager.py \
	BusyManager.py \
	ColorThemeMetadata.py \
	CommandLineInfo.py \
	CommandLineProcessor.py \
	CommandLineParser.py \
	CompletionWindowVisibilityManager.py \
	ContentDetector.py \
	CursorMetadata.py \
	DBusService.py \
	DialogFilters.py \
	DisplayRightMarginMetadata.py \
	Editor.py \
	EditorImports.py \
	Exceptions.py \
	FileChangeMonitor.py \
	FilenameGeneratorModeManager.py \
	FileModificationMonitor.py \
	FontMetadata.py \
	ForkScribesMetadata.py \
	FullScreenManager.py \
	GladeObjectManager.py \
	GlobalStore.py \
	InstanceManager.py \
	i18n.py \
	LanguageManager.py \
	LanguagePluginManager.py \
	License.py \
	Main.py \
	MarginPositionMetadata.py \
	MinimalModeMetadata.py \
	SchemeManager.py \
	ServicesInitializer.py \
	SIGNALS.py \
	SignalConnectionManager.py \
	SpellCheckMetadata.py \
	PluginSystemInitializer.py \
	PositionMetadata.py \
	TabWidthMetadata.py \
	TerminalSignalHandler.py \
	TextWrappingMetadata.py \
	Trigger.py \
	TriggerManager.py \
	URIManager.py \
	PluginManager.py \
	RegistrationManager.py \
	ReadonlyManager.py \
	RecentManager.py \
	Usage.py \
	UseTabsMetadata.py \
	UniqueStampGenerator.py \
	Utils.py \
	Word.py

clean-local:
	rm -rf *.pyc *.pyo

EXTRA_DIST = Globals.py.in 
