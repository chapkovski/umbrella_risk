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

from . import choices
author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'q'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
        # DEMOGRAPHICS
    age = models.StringField(label='What is your age?', choices=choices.AGE_CHOICES, widget=widgets.RadioSelect)
    education = models.StringField(
        label="What is the highest degree or level of school you have completed?",
        choices=choices.EDUCATION_CHOICES, widget=widgets.RadioSelect)
    gender = models.StringField(label='What is your gender?',
                                 choices=choices.GENDER_CHOICES, widget=widgets.RadioSelect)
    marital = models.StringField(label='What is your marital status?',
                                  choices=choices.MARITAL_CHOICES, widget=widgets.RadioSelect)
    employment = models.StringField(label='What is your current employment status?',
                                     choices=choices.EMPLOYMENT_CHOICES, widget=widgets.RadioSelect)
    income = models.StringField(
        label="What is your annual household income?",
        choices=choices.INCOME_CHOICES,
        widget=widgets.RadioSelect()
    )
 
    instructions_clarity = models.IntegerField(label="""
       How clear and understandable were the instructions to you? (Please write your answer between 1 = not understandable at all and 5 = completely understandable)
       """, choices=range(1, 6), widget=widgets.RadioSelectHorizontal)


    # big5 block
     # BFI-10 taken from Rammstedt and John 2007; https://doi.org/10.1016/j.jrp.2006.02.001
    big5_1 = models.IntegerField()
    big5_2 = models.IntegerField()
    big5_3 = models.IntegerField()
    big5_4 = models.IntegerField()
    big5_5 = models.IntegerField()
    big5_6 = models.IntegerField()
    big5_7 = models.IntegerField()
    big5_8 = models.IntegerField()
    big5_9 = models.IntegerField()
    big5_10 = models.IntegerField()
    
    # END OF BIG5 block