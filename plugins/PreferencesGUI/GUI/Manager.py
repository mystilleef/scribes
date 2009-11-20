class Manager(object):

	def __init__(self, manager, editor):
		from Window.Manager import Manager
		Manager(manager, editor)
		from SensitivityEmitter import Emitter
		Emitter(manager, editor)
		from FontButton import Button
		Button(manager, editor)
		from TabSpinButton import Button
		Button(manager, editor)
		from SpacesCheckButton import Button
		Button(manager, editor)
		from WrapCheckButton import Button
		Button(manager, editor)
		from MarginSpinButton import Button
		Button(manager, editor)
		from MarginCheckButton import Button
		Button(manager, editor)
		from SpellCheckButton import Button
		Button(manager, editor)
		from ResetButton import Button
		Button(manager, editor)
		from LanguageComboBox.Manager import Manager
		Manager(manager, editor)
