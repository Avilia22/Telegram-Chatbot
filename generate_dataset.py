#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- general imports --#
import json
import random


class Item_generator(object):

	"""This class allows random generation of items (such as teachers)

		Parameters:
			data(:obj:`list` or :obj:`str`): list of items or path to get the file with
				the data
			num_items(:obj:`int`): limit of items that the generator can generate

		Attributes:
			num_items(:obj:`int`): limit of items that the generator can generate
			items(:obj:`list`): list of the items that can be generated
	"""
	def __init__(self, data, num_items = 9999, name = False):
		self.name = name
		if isinstance(data, list):
			d_size = len(data)
			self.num_items = min(num_items, d_size)
			self.items = data[:self.num_items]
		else:
			d_size = len(open(data,'r').readlines())
			self.num_items = min(num_items, d_size)
			self.items = open(data,'r').readlines()[:self.num_items]
	"""
		Returns a random element of the item list
	"""
	def get_random(self):
		i_idx = random.randint(0, self.num_items-1)
		shorten = random.randint(0,100) <= 50;
		if shorten and self.name:
			length = random.randint(1, len(self.items[i_idx])-1)
			return ' '.join(self.items[i_idx].split(' ')[0:length])
		return self.items[i_idx]


class Data_generator(object):

	"""This class allows random generation of data (for instance, questions)

		Parameters:
			i_g(:class:`Item_generator`): Item generator for the data (items)
			s_g(:class:`Item_generator`): Item generator for the sentences (not items)
			type_(:type:`str`): can either be 'teacher' or 'subject', defines the type of item used
			intent(:type:`str`): defines the intent of the sentence to be generated

		Attributes:
			num_items(:obj:`int`): limit of items that the generator can generate
			items(:obj:`list`): list of the items that can be generated
	"""
	def __init__(self, i_g, s_g, type_, intent, language = 'ca'):
		if i_g: self.i_g = i_g
		else: self.i_g = None
		self.s_g = s_g
		self.type = type_
		self.intent = intent
		self.language = language

	"""
		Parameters:
			num_examples(:obj:`int`): defines the amount of examples to be generated

		This function returns a list (of size num_examples) of random generated examples
	"""
	def get_examples(self, num_examples):
		examples = []
		for i in range(num_examples):
			examples.append(self.get_random_element())
		return examples

	"""
		This function returns a random sentence generated with both generators
	"""
	def get_random_element(self):
		sentence = self.s_g.get_random()
		if self.intent == "ask_free_spots":
			chosen_grp = random.randint(10, 45)
			grp_str = "grup"
			if self.language == 'es': grp_str = "grupo"
			elif self.language == 'en': grp_str = "group"
			aux = grp_str+' {}'
			sentence = sentence.replace(aux, aux.format(chosen_grp))
		if self.i_g and "{}" in sentence:
			entity = self.i_g.get_random().lower().rstrip()
			offset_ini = 0
			for char in sentence:
				if char != "{":
					offset_ini += 1
				else: break
			offset_fi = offset_ini + len(entity)
			sentence = sentence.format(entity)
			if self.type == 'steering_committe': entity_type = 'steering_committe_name'
			if self.intent == "ask_free_spots" and grp_str in sentence:
				grp_start = sentence.find(grp_str)+len(grp_str)+1
				grp_end = grp_start+2;
				return {
					"text": sentence,
					"intent": self.intent,
					"entities": [
						{
							'start': offset_ini,
							'end': offset_fi,
							'value': entity,
							'entity': entity_type,
						},
						{
							'start': grp_start,
							'end': grp_end,
							'value': '{}'.format(chosen_grp),
							'entity': 'group',
						}
					]
				}
			else:
				return {
				"text": sentence.format(entity),
				"intent": self.intent,
				"entities": [
					{
						'start': offset_ini,
						'end': offset_fi,
						'value': entity,
						'entity': entity_type,
					}
				]
			}
		else:
			return {
				"text": sentence,
				"intent": self.intent
			}


def main(amount = 250, language = 'en'):
	random.seed(22)
	with open('Data/data_gen.json', 'rb') as jsonfile:
		data = json.load(jsonfile)[language]

	regex_features = [
		{
			"name": "group",
			"pattern": "([0-9]{2}|grup.|group)"
		},
		{
			"name": "plazas",
			"pattern": "(sitios|plazas|huecos|spots|places|matr.cula)"
		},
		{
			"name": "mail",
			"pattern": "(mail|corre.|email)"
		},
		{
			"name": "despacho",
			"pattern": "(despacho|oficina|office|despatx)"
		},
		{
			"name": "hora",
			"pattern": "(hora)"
		},
		{
			"name": "aula",
			"pattern": "(aula)"
		},
		{
			"name": "examen",
			"pattern": "(ex.m|test)"
		},
		{
			"name": "practicas",
			"pattern": "(pr.ct)"
		},
		{
			"name": "saludo",
			"pattern": "(hola|hello|buen|hey)"
		},
		{
			"name": "gracias",
			"pattern": "(gr.ci|thank|ty)"
		}
	]
	entity_synonyms = []
	common_examples = []

	steering_committe_gen = Item_generator(data = "./Data/steering_committe.txt", name = True)
	event_gen = Item_generator(data = "./Data/event.txt")

	intro_mail_gen = Item_generator(data = data['intros_steering_committe_mail'])
	intro_spots_gen = Item_generator(data = data['intros_event_free_spots'])
	intro_schedule_gen = Item_generator(data = data['intros_event_schedule'])
	intro_steering_committe_mail_gen = Item_generator(data = data['intros_steering_committe_mail'])
	intro_steering_committer_office_gen = Item_generator(data = data['intros_steering_committe_office'])
	intro_steering_committe_name_gen = Item_generator(data = data['intros_steering_committe_name'])
	intro_event_gen = Item_generator(data = data['intros_event'])
	intro_greet_gen = Item_generator(data = data['greet'])
	intro_thank_gen = Item_generator(data = data['thank'])

	steering_committe_mail_gen = Data_generator(steering_committe_gen, intro_mail_gen, type_="steering_committe", intent="ask_steering_committe_mail")
	event_spots_gen = Data_generator(event_gen, intro_spots_gen, type_="event", intent="ask_free_spots", language = language)
	event_schedule_gen = Data_generator(event_gen, intro_schedule_gen, type_="event", intent="ask_event_schedule")
	steering_committe_mail_gen = Data_generator(event_gen, intro_mail_gen, type_ ="event", intent = "ask_steering_committe_mail")
	steering_committe_office_gen = Data_generator(event_gen, intro_steering_committe_office_gen, type_ = "event", intent = "ask_steering_committe_office")
	steering_committe_name_gen = Data_generator(event_gen, intro_steering_committe_name_gen, type_="event", intent = "ask_steering_committe_name")
	next_event_gen = Data_generator(event_gen, intro_exams_gen, type_="event", intent = "ask_event")
	greet = Data_generator(None, intro_greet_gen, type_ = None, intent = "greet")
	thank = Data_generator(None, intro_thank_gen, type_ = None, intent = "thank")
	

	common_examples.extend( steering_committe_gen.get_examples(amount) )
	common_examples.extend( steering_committe_desk_gen.get_examples(amount) )
	common_examples.extend( event_spots_gen.get_examples(amount) )
	common_examples.extend( event_schedule_gen.get_examples(amount) )
	common_examples.extend( steering_committe_mail_gen.get_examples(amount) )
	common_examples.extend( steering_committe_office_gen.get_examples(amount) )
	common_examples.extend( steering_committe_name_gen.get_examples(amount) )
	common_examples.extend( next_event_gen.get_examples(amount) )
	common_examples.extend( greet.get_examples(amount) )
	common_examples.extend( thank.get_examples(amount) )

	file_path = './Data/Dataset_{}.json'.format(language)

	result = {"rasa_nlu_data": {
					"regex_features": regex_features,
					"entity_synonyms": entity_synonyms,
					"common_examples": common_examples}
			 }
	print ( "Size of the dataset: {}".format(len(common_examples)))
	json_ = str(json.dumps(result, indent=2))
	file = open(file_path,"w")
	file.write(json_)
	file.close()


if __name__ == "__main__":
	language = input("What language do you want to generate? (id/en/all)\n")
	if not (language == 'id' or language == 'en' or language == 'all'):
		language = None
	amount = input("How many examples for each type? ")
	if amount:
		if language == 'all':
			main(int(amount), 'id')
			main(int(amount), 'en')
		else: main(int(amount), language)
	else: main(language)
