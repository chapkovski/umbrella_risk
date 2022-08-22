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
        'bret',
        'cem',
        'mpl',
        'scl'
    ]



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
