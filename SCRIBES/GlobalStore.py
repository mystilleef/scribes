class Store(object):

	def __init__(self):
		self.__init_attributes()

	def __init_attributes(self):
		self.__object_dictionary = {}
		return

	def add_object(self, name, instance):
		from operator import contains
		from Exceptions import GlobalStoreObjectExistsError
		if contains(self.__object_dictionary.keys(), name): raise GlobalStoreObjectExistsError
		from utils import generate_random_number
		object_id = generate_random_number(map(lambda x: x[1],self.__object_dictionary.values()))
		self.__object_dictionary[name] = instance, object_id
		return object_id

	def remove_object(self, name, object_id):
		from Exceptions import GlobalStoreObjectDoesNotExistError
		from operator import ne
		if ne(object_id, self.__object_dictionary[name][1]): raise GlobalStoreObjectDoesNotExistError
		del self.__object_dictionary[name]
		return

	def get_object(self, name):
		try:
			instance = self.__object_dictionary[name]
		except KeyError:
			from Exceptions import GlobalStoreObjectDoesNotExistError
			raise GlobalStoreObjectDoesNotExistError
		return instance[0]

	def list_objects(self):
		object_names = []
		object_names = self.__object_dictionary.keys()
		object_names.sort()
		return object_names

	def __destroy(self):
		self.__object_dictionary.clear()
		del self
		self = None
		return
