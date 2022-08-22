from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import random
import json
import itertools

author = 'Philipp Chapkovski, WZB'

doc = """
Umbrella app for several risk measures
"""


class Constants(BaseConstants):
    name_in_url = 'umbrella'
    players_per_group = None
    num_rounds = 3
    TREATMENTS = [
        'risk',
        'ambiguity',
        'control'
    ]
    APPS = [
        'BRET',
        'CEM',
        'MPL',
        'SCL'
    ]



class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number==1:
            for p in self.session.get_participants():
                treatments = Constants.TREATMENTS.copy()
                random.shuffle(treatments)
                p.vars['treatments'] = treatments
                apps = Constants.APPS.copy()
                random.shuffle(apps)
                p.vars['appseq']  = apps

        for p in self.get_players():
            p.treatment = p.participant.vars['treatments'][self.round_number-1]
            p.appseq = json.dumps(p.participant.vars['appseq'])



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField()
    appseq = models.StringField()
    def get_apps(self):
        return self.participant.vars['appseq']