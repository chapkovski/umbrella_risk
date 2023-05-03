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
    treatment_correspodence = dict(
        control=dict(cover=False,
                     risk=lambda x: 100),
        risk=dict(cover=False,
                  risk=lambda x: x.session.config.get('risk', 50)),
        ambiguity=dict(cover=True,
                       risk=lambda x: random.choice(range(0, 101, 10)))
    )


class Subsession(BaseSubsession):

    def bret_creating_session(self):
        pass

    def creating_session(self):

        session_creator.bret.creating_session(self)
        session_creator.cem.creating_session(self)
        session_creator.mpl.creating_session(self)
        session_creator.scl.creating_session(self)

        if self.round_number == 1:
            for p in self.session.get_participants():
                treatments = Constants.TREATMENTS.copy()
                random.shuffle(treatments)
                p.vars['treatments'] = treatments
                apps = Constants.APPS.copy()
                random.shuffle(apps)
                p.vars['appseq'] = apps
                p.vars['payable_app'] = random.choice(apps)
                p.vars['payable_round'] = random.randint(1, Constants.num_rounds)
                p.vars['lottery_outcome'] = random.uniform(0,360)

        for p in self.get_players():
            p.treatment = p.participant.vars['treatments'][self.round_number-1]
            p.appseq = json.dumps(p.participant.vars['appseq'])
            treatment_params = Constants.treatment_correspodence[p.treatment]
            p.risk = treatment_params.get('risk')(p)
            p.cover = treatment_params.get('cover')
            p.payable_app=p.participant.vars.get('payable_app')
            p.payable_round=p.participant.vars.get('payable_round')
            p.lottery_outcome=p.participant.vars.get('lottery_outcome')

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    bret_payoff = models.CurrencyField()
    cem_payoff = models.CurrencyField()
    mpl_payoff = models.CurrencyField()
    scl_payoff = models.CurrencyField()
    consent = models.BooleanField(
        widget=widgets.CheckboxInput, label='I have read this consent form and I agree')
    treatment = models.StringField()
    appseq = models.StringField()
    cover = models.BooleanField()
    risk = models.IntegerField()
    payable_round = models.IntegerField()
    payable_app = models.StringField()
    lottery_outcome = models.FloatField()

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
        locals()['mpl_choice_' + str(j)] = models.StringField()
    del j

    mpl_random_draw = models.IntegerField()
    mpl_choice_to_pay = models.StringField()
    mpl_option_to_pay = models.StringField()
    mpl_inconsistent = models.IntegerField()
    mpl_switching_row = models.IntegerField()

    ##############################END OF MPL###############################

    ##############################QUIZES###############################
    cq_1 = models.StringField(label='At the end of the study, how many decisions will be paid out?',
                              choices=[str(i) for i in range(1, 13)], widget=widgets.RadioSelect)
    cq_2 = models.StringField(label='Does the decision in one part of the experiment influence the outcome of other parts?',
                              choices=['Yes', 'No'], widget=widgets.RadioSelect)
    cq_control = models.StringField(label=' How likely is it, that you receive an additional 5€?',
                                    choices=[f'{i}%' for i in range(
                                        0, 101, 10)]+['I do not know'],
                                    widget=widgets.RadioSelect)
    cq_risk = models.StringField(label='How likely is it, that you receive an additional 10€?',
                                 choices=[f'{i}%' for i in range(
                                     0, 101, 10)]+['I do not know'],
                                 widget=widgets.RadioSelect)
    cq_ambiguity = models.StringField(label='How likely is it, that you receive an additional 10€?',
                                      choices=[f'{i}%' for i in range(
                                          0, 101, 10)]+['I do not know'],
                                      widget=widgets.RadioSelect)
    ##############################END OF MPL###############################
