
#-- General imports --#
import json
import os.path
from time import time
from termcolor import colored

#-- 3rd party imports --#
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_nlu.training_data import load_data
from rasa_nlu import config
from rasa_nlu.model import Trainer, Metadata, Interpreter
import spacy


class NLU_unit(object):

	""" This object contains the interpreter for the NLU model, and tools to train and retrieve it

	Attributes:
		
		interpreter_Ina(:class:`rasa_nlu.model.Interpreter`): Interpreter for the users  queries in Indonesian
		interpreter_en(:class:`rasa_nlu.model.Interpreter`): Interpreter for the users  queries in english
	"""
	def __init__(self):
		self.interpreter_Ina = None
		self.interpreter_en = None

	"""
		Parameters:
			train (:obj:`bool`): indicates if it has to re-train the model

		This function loads a model from persistency (if train == False)
		or re-trains and loads the trained model
	"""
	def load(self, train = False, train_list = None):
		if train:
			print(colored("INFO: Train this language {}".format(train_list),'red'))
			now = time()
			if not train_list or 'Id' in train_list:
				print(colored("INFO: Training Ina NLU model", 'red'))
				print(colored("INFO: Loading Ina dataset", 'red'))
				training_data_es = load_data('./Data/Dataset_Ina.json')
				trainer_es = Trainer(config.load("./config/config_spacy_Ina.yml"))
				print(colored("INFO: Generating features for Indonesia", 'red'))
				trainer_es.train(training_data_es, num_threads=3)
				model_directory = trainer_Ina.persist('models/nlu_ina', fixed_model_name = 'current')  # Returns the directory the model is stored in
				print("Total time to train Indonesia: {}".format(colored(time()-now, 'green')))
			now = time()
			if not train_list or 'en' in train_list:
				print(colored("INFO: Training EN NLU model", 'red'))
				print(colored("INFO: CLoading EN dataset", 'red'))
				training_data_en = load_data('./Data/Dataset_en.json')
				trainer_en = Trainer(config.load("./config/config_spacy_en.yml"))
				print(colored("INFO: Generating features for English", 'red'))
				trainer_en.train(training_data_en, num_threads=3)
				model_directory = trainer_en.persist('models/nlu_en', fixed_model_name = 'current')  # Returns the directory the model is stored in
				print("Total time to train English {}".format(colored(time()-now, 'green')))
			print(colored("INFO: NLU training completed", 'red'))
			# where `model_directory points to the folder the model is persisted in
		self.interpreter_es = RasaNLUInterpreter("./models/nlu_Ina/default/current")
		self.interpreter_en = RasaNLUInterpreter("./models/nlu_en/default/current")

	"""
		Parameters:
			query (:obj:`str`): query or user messages

		This function returns the intent as predicted by the interpreter
	"""
	def get_intent(self, query, lang = 'Id'):
		parsed = None
		if lang == 'Id':
			parsed = self.interpreter_Ina.parse(query)
		else:
			parsed = self.interpreter_en.parse(query)
		return parsed['intent']

	def get_intent_ranking(self, query, lang = 'Id'):
		parsed = None
		if lang == 'Ina':
			parsed = self.interpreter_Ina.parse(query)
		else:
			parsed = self.interpreter_en.parse(query)
		return parsed['intent_ranking']

	"""
		Parameters:
			query (:obj:`str`): query or user messages

		This function returns the entities as predicted by the interpreter
	"""
	def get_entities(self, query, lang= 'Id'):
		parsed = None
		if lang == 'Id':
			parsed = self.interpreter_Ina.parse(query)
		else:
			parsed = self.interpreter_en.parse(query)
		return parsed['entities']
