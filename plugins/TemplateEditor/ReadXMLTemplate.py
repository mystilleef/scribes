# -*- coding: utf-8 -*-
# Copyright © 2005 Lateef Alabi-Oki
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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

def get_template_from_file(filename):
	"""
	Get templates from an XML template file.

	@param filename: The path to an XML template file.
	@type filename: A String object.

	@return: Template information contained in an XML file or nothing.
	@rtype: A List object.
	"""
	from Exceptions import InvalidFileError
	if is_xml_file(filename) is False: raise InvalidFileError
	from xml.dom.minidom import parse
	xml_document = parse(filename)
	validate_xml_document(xml_document)
	templates = get_templates(xml_document)
	return templates

def get_template_from_string(string):
	"""
	Get templates from an XML template string.

	@param string: A string containing XML template information.
	@type string: A String object.

	@return: Template information contained in an XML file or nothing.
	@rtype: A List object.
	"""
	from xml.dom.minidom import parseString
	xml_document = parseString(string)
	validate_xml_document(xml_document)
	templates = get_templates(xml_document)
	xml_document.unlink()
	return templates

def is_xml_file(filename):
	"""
	Check whether or not a file is an XML file.

	@param filename: The path to a file.
	@type filename: A String object.

	@return: True if the file is an XML file.
	@rtype: A Boolean object.
	"""
	from gnomevfs import get_uri_from_local_path, exists, get_mime_type
	uri = get_uri_from_local_path(filename)
	if exists(uri) is False: return False
	if get_mime_type(uri) in ["text/xml", "application/xml"]: return True
	return False

def validate_xml_document(xml_document):
	"""
	Check whether or not the xml document is a recognizable template
	format for the text editor.

	@param xml_document: An object representing an XML document.
	@type xml_document: An xml.dom.minidom.Document object.

	@return: True if validation succeeds.
	@rtype: A Boolean object.
	"""
	from Exceptions import ValidationError
	root_element = xml_document.documentElement
	if root_element.localName in ["snippet"] is False: raise ValidationError
	if not root_element.getElementsByTagName("entry"): raise ValidationError
	if not root_element.getElementsByTagName("trigger"): raise ValidationError
	if not root_element.getElementsByTagName("description"): raise ValidationError
	if not root_element.getElementsByTagName("template"): raise ValidationError
	trigger_nodes = root_element.getElementsByTagName("trigger")
	for trigger_element in trigger_nodes:
		if trigger_element.hasAttribute("id") is False: raise ValidationError
		if not trigger_element.getAttribute("id"): raise ValidationError
		if not trigger_element.firstChild.data: raise ValidationError
	return

def get_templates(xml_document):
	"""
	Get templates from an xml document object.

	@param xml_document: An object representing an XML document.
	@type xml_document: An xml.dom.minidom.Document object.

	@return: Templates in an xml document.
	@rtype: A List object.
	"""
	templates = []
	root_element = xml_document.documentElement
	entry_nodes = root_element.getElementsByTagName("entry")
	for entry_element in entry_nodes:
		template = get_template_from_element(entry_element)
		templates.append(template)
	return templates

def get_template_from_element(entry_element):
	"""
	Get template information associated with an entry element in an
	xml document object.

	@param entry_element: An element in an XML document object.
	@type entry_element: An Element object.

	@return: Data for a template.
	@rtype: A Tuple object.
	"""
	trigger_element = entry_element.getElementsByTagName("trigger")[0]
	trigger = trigger_element.firstChild.data
	trigger_attribute_value = language = trigger_element.getAttribute("id")
	template_key = trigger_attribute_value + trigger
	description_element = entry_element.getElementsByTagName("description")[0]
	description = ""
	if description_element.firstChild:
		description = description_element.firstChild.data
	template_element = entry_element.getElementsByTagName("template")[0]
	template = ""
	if template_element.firstChild:
		template = template_element.firstChild.data
	template_data = template_key, description, template, language.lower()
	return template_data
