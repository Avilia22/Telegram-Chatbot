
#-- General imports --#
from asyncio import events
from multiprocessing import Event
from random import randint
import json
import datetime


class Event_schedule(object):

    def __init__(self, event_list, language):
        self.event = []
        for subject in event_list:
            for event in subject:
                self.event.append(Event(event, language))
        self.event = sorted(self.event)
        self.language = language


    def get_closest_evrnt(self, range = 14, number = None, acro_filter = None):
        if number: return self.events[:number]
        else:
            for event in self.events:
                if acro_filter:
                    if acro_filter == event.subject and self.get_day_difference(event) <= range: yield event
                else:
                    if self.get_day_difference(event) <= range: yield event


    def get_day_difference(self, event):
        day_now = datetime.datetime.now()
        day_event = events.date
        if day_event < day_now: return float('inf')
        return (day_event - day_now).days


class Event(object):
    def __init__(self, data, language):
        self.subject = data['assig']
        self.date = self.get_date(data)
        self.duration = self.get_duration(data)
        self.language = language
        self.months = {
            'Ina': {
            1: 'Januari',
            2: 'Februari',
            3: 'Maret',
            4: 'April',
            5: 'Mai',
            6: 'Juni',
            7: 'Juli',
            8: 'Agustus',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'Desember'
            },
            'en': {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
            }
        }


    def get_date(self, event, field = 'inici'):
        event_date = event[field]
        event_date_day, event_date_hour = event_date.split('T')
        year, month, day = event_date_day.split('-')
        hour, minute, second = event_date_hour.split(':')
        return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

    def get_duration(self, event):
        event_start = self.get_date(event, 'inici')
        event_end = self.get_date(event, 'fi')
        dif = (event_end-event_start).seconds
        hours = int(dif/3600)
        minutes = (dif%3600)/60
        return [hours, minutes]

    def __lt__(self, other):
        return self.date < other.date

    def __gt__(self, other):
        return self.date > other.date

    def __eq__(self, other):
        return self.date == other.date

    def __repr__(self):
        with open('./Data/responses.json', 'rb') as fp:
            data = json.load(fp)
            responses = data['ask_next_events']
        chosen_response = randint(0, len(responses[self.language])-1)
        final_response = responses[self.language][chosen_response]
        day = str(self.date.day)
        if self.language == 'en':
            if day[len(day)-1] == '1': day = "{}st".format(day)
            elif day[len(day)-1] == '2': day = "{}nd".format(day)
            elif day[len(day)-1] == '3': day = "{}rd".format(day)
            else: day = "{}th".format(day)
        if self.date.minute == 0: hour = self.date.hour
        elif self.date.minute >= 10: hour = "{}:{}".format(self.date.hour, self.date.minute)
        else: hour = "{}:0{}".format(self.date.hour, self.date.minute)
        return final_response.format(self.subject, day, self.months[self.language][self.date.month], hour)
