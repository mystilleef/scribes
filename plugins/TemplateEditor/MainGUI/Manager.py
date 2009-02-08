class Manager(object):

	def __init__(self, manager, editor):
		from Window import Window
		Window(manager, editor)
		from SourceView import SourceView
		SourceView(manager, editor)
		from HelpButton import Button
		Button(manager, editor)
		from LinkButton import Button
		Button(manager, editor)
		from ImportButton import Button
		Button(manager, editor)
		from RemoveButton import Button
		Button(manager, editor)
		from ExportButton import Button
		Button(manager, editor)
		from EditButton import Button
		Button(manager, editor)
		from DescriptionTreeView import TreeView
		TreeView(manager, editor)
		from DescriptionTreeViewSelector import Selector
		Selector(manager, editor)
		from DescriptionTreeViewGenerator import Generator
		Generator(manager, editor)
		from AddButton import Button
		Button(manager, editor)
		from LanguageTreeView import TreeView
		TreeView(manager, editor)
		from LanguageTreeViewModelGenerator import Generator
		Generator(manager, editor)
