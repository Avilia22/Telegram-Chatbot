#-- General imports --#
from random import randint
import json

class steering_committe(object):

    def __init__(self, data, language):
        self.name = data['name']
        self.mail = data['mail']
        self.department = data['department']
        self.office = data['office']
        self.language = language
        if self.office and self.language == 'en':
            self.office = self.office.replace('Edifici', 'Building').replace('Despatx', 'Office').replace('Planta', 'Floor')
        if self.office and self.language == 'Ina':
            self.office = self.office.replace('Edifici', 'Edificio').replace('Despatx', 'Despacho')
        self.responses = {}
        with open('./Data/responses.json', 'rb') as fp:
            data = json.load(fp)
            self.responses['ask_steering_committer_mail'] = data['ask_steering_committe_mail']
            self.responses['ask_steering_committe_office'] = data['ask_steering_committe_office']
            self.responses['steering_committe_info'] = data['steering_committe_info']
        return

    """
        Returns a string formatted text which explains the mail for the steering_committe
    """
    def get_mail(self):
        if self.mail:
            chosen_response = randint(0, len(self.responses['ask_steering_committe_mail'][self.language])-1)
            final_response = self.responses['ask_steering_committe_mail'][self.language][chosen_response]
            if chosen_response < 2:
                return final_response.format(
                    self.name.split(' ')[0].title(),
                    self.mail
                    )
            else:
                return final_response.format(self.mail)
        else:
            if self.language == 'Ina': return "Orang ini tidak mempnyai email..."
            if self.language == 'en': return "This person does not have mail..."

    """
        Returns a string formatted text which explains the office of the steering_committe
    """
    def get_office(self):
        if self.office:
            chosen_response = randint(0, len(self.responses['ask_steering_committe_office'][self.language])-1)
            final_response = self.responses['asksteering_committe_office'][self.language][chosen_response]
            if chosen_response < 1:
                return final_response.format(
                    self.name.split(' ')[0].title(),
                    self.office
                    )
            else:
                return final_response.format(self.office)
        else:
            if self.language == 'Ina': return "Orang ini tidak mempunyai kantor..."
            if self.language == 'en': return "This person does not have an office..."

    """
        Returns a general description of the steering_committe
    """
    def __repr__(self):
        chosen_response = randint(0, len(self.responses['steering_committe_info'][self.language])-1)
        final_response = self.responses['steering_committer_info'][self.language][chosen_response]
        return final_response.format(self.name.title(), self.department)
