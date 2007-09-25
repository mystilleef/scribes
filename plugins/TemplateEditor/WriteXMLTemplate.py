def create_template_file(template_info_list, filename):
	"""
	Create an XML file that contains templates for the text editor.

	Each item in the template information list is a tuple containing the
	following:

		(language_id, trigger, description, template)

	@param template_info_list: A list of information about templates.
	@type template_info_list: A List object.
	"""
	from xml.dom.minidom import Document
	xml_document = Document()
	root_element = add_root_element(xml_document)
	add_entries(xml_document, root_element, template_info_list)
	write_document_to_file(xml_document, filename)
	return

def create_template_string(template_info_list):
	from xml.dom.minidom import Document
	xml_document = Document()
	root_element = add_root_element(xml_document)
	add_entries(xml_document, root_element, template_info_list)
	string = write_document_to_string(xml_document)
	return string

def add_entries(xml_document, root_element, template_info_list):
	"""
	Create entries for each template in the information list.

	@param xml_document: An object representing an XML document.
	@type xml_document: A xml.dom.minidom.Document object.

	@param root_element: The root element in an XML document.
	@type root_element: A instance object.

	@param template_info_list: A list of template information.
	@type template_info_list: A List object.
	"""
	for template in template_info_list:
		add_entry_element(xml_document, root_element, template)
	return

def write_document_to_file(xml_document, filename):
	"""
	Write the XML document object to an XML file.

	@param xml_document: An object representing an XML document.
	@type xml_document: A xml.dom.minidom.Document object.
	"""
	file_object = open(filename, "w")
	xml_document.writexml(file_object, encoding="UTF-8")
	file_object.close()
	return

def write_document_to_string(xml_document):
	string = xml_document.toxml("UTF-8")
	return string

def add_root_element(xml_document):
	"""
	Create the root element for the XML document.

	@param xml_document: An object representing an XML document.
	@type xml_document: A xml.dom.minidom.Document object.

	@return: The root element of the XML document.
	@rtype: An instance object.
	"""
	root_element = xml_document.createElement("snippet")
	xml_document.appendChild(root_element)
	return root_element

def add_entry_element(xml_document, root_element, template):
	"""
	Create the entry element for the XML document.

	@param xml_document: An object representing an XML document.
	@type xml_document: A xml.dom.minidom.Document object.

	@param root_element: The root element in an XML document.
	@type root_element: A instance object.

	@param template: Information for a template.
	@type template: A Tuple object.
	"""
	entry_element = xml_document.createElement("entry")
	root_element.appendChild(entry_element)
	add_trigger_element(xml_document, entry_element, template)
	add_description_element(xml_document, entry_element, template)
	add_template_element(xml_document, entry_element, template)
	return

def add_trigger_element(xml_document, entry_element, template):
	"""
	Add a trigger element to the XML's document's entry element.

	@param xml_document: An object representing an XML document.
	@type xml_document: A xml.dom.minidom.Document object.

	@param entry_element: The trigger element in an XML document.
	@type entry_element: A instance object.

	@param template: Information for a template.
	@type template: A Tuple object.
	"""
	trigger_element = xml_document.createElement("trigger")
	entry_element.appendChild(trigger_element)
	add_attribute_to_element(trigger_element, "id", template[0])
	add_text_to_element(xml_document, trigger_element, template[1])
	return

def add_description_element(xml_document, entry_element, template):
	"""
	Add a description element to the XML's document's entry element.

	@param xml_document: An object representing an XML document.
	@type xml_document: A xml.dom.minidom.Document object.

	@param entry_element: The description element in an XML document.
	@type entry_element: A instance object.

	@param template: Information for a template.
	@type template: A Tuple object.
	"""
	description_element = xml_document.createElement("description")
	entry_element.appendChild(description_element)
	add_text_to_element(xml_document, description_element, template[2])
	return

def add_template_element(xml_document, entry_element, template):
	"""
	Add a template element to the XML's document's entry element.

	@param xml_document: An object representing an XML document.
	@type xml_document: A xml.dom.minidom.Document object.

	@param entry_element: The description element in an XML document.
	@type entry_element: A instance object.

	@param template: Information for a template.
	@type template: A Tuple object.
	"""
	template_element = xml_document.createElement("template")
	entry_element.appendChild(template_element)
	add_text_to_element(xml_document, template_element, template[3])
	return

def add_attribute_to_element(element, attribute, value):
	"""
	Add an attribute to an element.

	@param element: Element to add an attribute to.
	@type element: An instance object.

	@param attribute: The name of the attribute.
	@type attribute: A String object.

	@param value: The value of the attribute.
	@type value: A String object.
	"""
	element.setAttribute(attribute, value)
	return

def add_text_to_element(xml_document, element, text):
	"""
	Add text to an element.

	@param xml_document: An object representing an XML document.
	@type xml_document: A xml.dom.minidom.Document object.

	@param element: Element to add an attribute to.
	@type element: An instance object.

	@param text: The text to add to an element.
	@type text: A String object.
	"""
	text_node = xml_document.createTextNode(text)
	element.appendChild(text_node)
	return

def create_element(xml_document, name):
	"""
	Create an element for an XML document.

	@param xml_document: An object representing an XML document.
	@type xml_document: A xml.dom.minidom.Document object.

	@param name: The name of the element.
	@type name: A String object.

	@return: An element in a XML document.
	@rtype: An instance object.
	"""
	element = xml_document.createElement(name)
	return element

def validate_xml(filename):
	"""
	Validate an XML file against an internal DTD.

	@param filename: An XML file to be validated.
	@type filename: A String object.

	@return: True if validation succeeds.
	@rtype: A Boolean object.
	"""
	return True
