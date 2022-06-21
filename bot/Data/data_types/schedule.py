
#-- General imports --#
from random import randint
import json
import datetime


class Schedule(object):

    def __init__(self, data, language, event):
        self.event = []
        self.language = language
        for event in data:
            self.event.append(event(event, self.language))
        with open('./Data/responses.json', 'rb') as fp:
            data = json.load(fp)
            self.responses = data['ask_next_event']
        return


    def get_next_event(self):
        now = datetime.date.today().isoweekday()
        hour = datetime.datetime.now().hour
        checker = [now, hour]
        ok = []
        for event in self.events:
            if event.day_schedule > checker: ok.append(event)
        if not ok: return []
        else: return min(ok)

    def get_response(self):
        now = datetime.date.today().isoweekday()
        hour = datetime.datetime.now().hour
        next = self.get_next_event()
        if not next: return self.responses[self.language]["other_day_other_week"]
        else:
            schedule = next.day_schedule
            if now == schedule[0]:
                chosen_response = randint(0, len(self.responses[self.language]['same_day'])-1)
                final_response = self.responses[self.language]['same_day'][chosen_response]
                return final_response.format(next.assig, schedule[1], next.classroom)
            else:
                chosen_response = randint(0, len(self.responses[self.language]['other_day_week'])-1)
                final_response = self.responses[self.language]['other_day_week'][chosen_response]
                if schedule[0]-now == 1: return final_response.format(self.get_tomorrow(), next.assig, schedule[1], next.classroom)
                else:
                    return final_response.format(self.get_following_days().format(schedule[0]-now), next.assig, schedule[1], next.classroom)

class Events(object):

    
    def __init__(self, data, language):
        days = {
        
            'Ina': {
                1: 'Senin',
                2: 'Selasa',
                3: 'Rabu',
                4: 'Kmis',
                5: 'Jumat',
                6: 'Sabtu',
                7: 'Minggu'
            },
            'en': {
                1: 'Monday',
                2: 'Tuesday',
                3: 'Wednesday',
                4: 'Thursday',
                5: 'Friday',
                6: 'Saturday',
                7: 'Sunday'
            }
        }
        self.day_schedule = [data['dia_setmana'], self.format_hour(data['inici'])]
        self.language = language
        self.assig = data['codi_assig']
        self.group = data['grup']
        self.day = days[self.language][data['dia_setmana']]
        self.begin_hour = data['inici']
        aux_hour =  self.begin_hour.split(':')
        self.end_hour = "{}:{}".format(
                str(int(aux_hour[0])+data['durada']),
                aux_hour[1] )
        with open('./Data/responses.json', 'rb') as fp:
            data = json.load(fp)
            self.responses = data['ask_subject_schedule']
        return


    def __repr__(self):
        chosen_response = randint(0, len(self.responses[self.language])-1)
        final_response = self.responses[self.language][chosen_response]
        return final_response.format(
            self.day,
            self.begin_hour,
            self.end_hour,
        )

    def format_hour(self, hour):
        return int(hour.split(':')[0])

    def __lt__(self, other):
        return self.day_schedule < other.day_schedule

    def __gt__(self, other):
        return self.day_schedule > other.day_schedule

    def __eq__(self, other):
        return self.day_schedule == other.day_schedule
