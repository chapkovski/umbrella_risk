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
from .configs.cem import Constants as CEM_Constants
from .configs.mpl import Constants as MPL_Constants
import random
import json
import itertools
from umbrella import session_creator
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
    def bret_creating_session(self):
        pass

    def creating_session(self):
        session_creator.bret.creating_session(self)
        session_creator.cem.creating_session(self)
        session_creator.mpl.creating_session(self)
        session_creator.scl.creating_session(self)


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

    ##############################BRET###############################
    bret_bomb = models.IntegerField()
    bret_bomb_row = models.PositiveIntegerField()
    bret_bomb_col = models.PositiveIntegerField()
    bret_boxes_collected = models.IntegerField()
    bret_boxes_scheme = models.StringField()

    ##############################END OF BRET###############################
    ##############################CEM###############################
    # add model fields to class player
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    for j in range(1, CEM_Constants.num_choices + 1):
        locals()['cem_choice_' + str(j)] = models.StringField()
    del j

    cem_random_draw = models.IntegerField()
    cem_choice_to_pay = models.StringField()
    cem_option_to_pay = models.StringField()
    cem_inconsistent = models.IntegerField()
    cem_switching_row = models.IntegerField()


    ##############################END OF CEM###############################

    ##############################SCL###############################
    # add model fields to class player
    # ----------------------------------------------------------------------------------------------------------------
    scl_lottery_choice = models.IntegerField()
    scl_outcome_to_pay = models.StringField()
    ##############################END OF SCL###############################

    ##############################MPL###############################

    for j in range(1, MPL_Constants.num_choices + 1):
        locals()['mcl_choice_' + str(j)] = models.StringField()
    del j


    mcl_random_draw = models.IntegerField()
    mcl_choice_to_pay = models.StringField()
    mcl_option_to_pay = models.StringField()
    mcl_inconsistent = models.IntegerField()
    mcl_switching_row = models.IntegerField()


    ##############################END OF MPL###############################