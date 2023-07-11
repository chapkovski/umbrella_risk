from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as cu, currency_range
)
from cem.config import *
import random
from random import randrange


author = 'Felix Holzmeister'

doc = """
Certainty equivalent method as proposed by Cohen et al. (1987) and Abdellaoui et al. (2011),
as well as variations thereof suggested by Bruner (2009) and Gächter et al. (2010).
"""


# ******************************************************************************************************************** #
# *** CLASS CONSTANTS *** #
# ******************************************************************************************************************** #
class Constants(BaseConstants):

    # ---------------------------------------------------------------------------------------------------------------- #
    # --- Task-specific Settings --- #
    # ---------------------------------------------------------------------------------------------------------------- #

    # type of variation
    # the app allows to vary one of the following parameters: the sure payoff, the probability of the high payoff,
    # or the high or low lottery payoff; the remaining three parameters are held constant for all choices
    # possible values for <variation> are 'sure_payoff' (Cohen et al., 1987; Abdellaoui et al., 2011)
    # 'probability' (Bruner, 2009), 'lottery_hi' (Bruner, 2009), or 'lottery_lo' (Gächter et al., 2007)
    variation = 'sure_payoff'

    # number (n) of choices with <i = 1, 2, ..., n>
    # <num_choices> determines how many choices between a lottery and a sure payoff shall be implemented
    num_choices = 9

    # "high" and "low" payoffs (in currency units set in settings.py) of the lottery "option A"
    # the lottery payoffs remain constant if <variation = 'sure_payoff'> or <variation = 'probability'>
    # if <variation = 'lottery_hi'>, <lottery_hi> constitutes the high lottery payoff for the first choice
    # for subsequent choices <i>, the high lottery outcome is determined by <lottery_hi> + <i-1> * <step_size>
    # if <variation = 'lottery_lo'>, <lottery_lo> constitutes the low lottery payoff for the first choice
    # for subsequent choices <i>, the high lottery outcome is determined by <lottery_lo> - <i-1> * <step_size>
    lottery_hi = 3 #15.00
    lottery_lo = 1 #5.00

    # probability of lottery outcome "high" in %
    # the probability of lottery payoffs is constant if <variation = 'sure_payoff'> or <variation = 'lottery_*'>
    # if <variation = 'probability'>, <probability> determines the likelihood of the high payoff in the first choice
    # for subsequent choices <i>, the probability is determined by <probability> + <i-1> * <step_size>
    probability = 50

    # sure payoff ("option B")
    # the sure payoff remains constant if <variation = 'probability'> or <variation = 'lottery_*'>
    # if <variation = 'sure_payoff'>, <sure_payoff> constitutes the certain payment ("option B") in the first choice
    # for subsequent choices <i>, the certain payment is determined by <sure_payoff> + <i-1> * <step_size>
    sure_payoff = 1 #5.00

    # step size (in units of the parameter defined in <variation>)
    # the variable <variation> defines which of the four parameters is varied across the <num_choices> choices
    # <step_size> constitutes the increment in terms of the varying parameter (while the remaining three are constant)
    # thus, the varying parameter for choice i = 1, 2, ..., n, <var_i>, is defined by <var> + <i-1> * <step_size>
    # if <variation> is set to 'sure_payoff', 'lottery_hi', or 'lottery_lo', <step_size> is in currency units
    # if <variation> is set to 'probability', <step_size> is in percentage units (i.e. <step_size>%)
    step_size = .5

    # initial endowment (in currency units set in settings.py)
    # <endowment> defines an additional endowment for the task to capture potential losses if <variation = lottery_lo>
    # if no additional endowment should be implemented, set <endowment> to 0
    endowment = 0.00

    # ---------------------------------------------------------------------------------------------------------------- #
    # --- Overall Settings and Appearance --- #
    # ---------------------------------------------------------------------------------------------------------------- #

    # do not display certain payoff and ask for whether to accept or reject the lottery
    # if <accept_reject = False>, subjects face a table with a lottery on the left and a sure payoff on the right
    # if <accept_reject = True>, only the lottery will be displayed in the table but not the sure payoff
    # subjects are asked to indicate whether they want to accept or to reject each of the lotteries
    # note that <accept_reject = True> is only implementable if <variation> is set to 'probability' or 'lottery_*'
    # if <accept_reject = True>, choice = "A" refers to acceptance while choice = "B" refers to rejection
    accept_reject = False

    # show each lottery pair on a separate page
    # if <one_choice_per_page = True>, each single binary choice between lottery "A" and "B" is shown on a separate page
    # if <one_choice_per_page = False>, all <num_choices> choices are displayed in a table on one page
    one_choice_per_page = False

    # order choices between lottery pairs randomly
    # if <random_order = True>, the ordering of binary decisions is randomized for display
    # if <random_order = False>, binary choices are listed in ascending order of the probability of the "high" outcome
    random_order = False

    # enforce consistency, i.e. only allow for a single switching point
    # if <enforce_consistency = True>, all options "A" above a selected option "A" are automatically selected
    # similarly, all options "B" below a selected option "B" are automatically checked, implying consistent choices
    # note that <enforce_consistency> is only implemented if <one_choice_per_page = False> and <random_order = False>
    enforce_consistency = True

    # show progress bar
    # if <progress_bar = True> and <one_choice_per_page = True>, a progress bar is rendered
    # if <progress_bar = False>, no information with respect to the advance within the task is displayed
    # the progress bar graphically depicts the advance within the task in terms of how many decision have been made
    # further, information in terms of "page x out of <num_choices>" (with x denoting the current choice) is provided
    progress_bar = True

    # show instructions page
    # if <instructions = True>, a separate template "Instructions.html" is rendered prior to the task
    # if <instructions = False>, the task starts immediately (e.g. in case of printed instructions)
    instructions = True

    # show results page summarizing the task's outcome including payoff information
    # if <results = True>, a separate page containing all relevant information is displayed after finishing the task
    # if <results = False>, the template "Decision.html" will not be rendered
    results = False

    # ---------------------------------------------------------------------------------------------------------------- #
    # --- oTree Settings (Don't Modify) --- #
    # ---------------------------------------------------------------------------------------------------------------- #

    name_in_url = 'cem'
    players_per_group = None
    num_rounds = num_choices if one_choice_per_page else 1


# ******************************************************************************************************************** #
# *** CLASS SUBSESSION
# ******************************************************************************************************************** #
class Subsession(BaseSubsession):

    # initiate lists before session starts in round 1
    # ----------------------------------------------------------------------------------------------------------------
    def creating_session(self):
        if self.round_number == 1:

            n = Constants.num_choices
            for p in self.get_players():

                # create list of lottery indices
                # ----------------------------------------------------------------------------------------------------
                indices = [j for j in range(1, n + 1)]

                # create list corresponding to form_field variables including all choices
                # ----------------------------------------------------------------------------------------------------
                form_fields = ['choice_' + str(k) for k in indices]

                # create list of probabilities
                # ----------------------------------------------------------------------------------------------------
                if Constants.variation == 'probability':
                    probabilities = [Constants.probability + (k - 1) * Constants.step_size for k in indices]
                else:
                    probabilities = [Constants.probability for k in indices]

                # create list of high lottery payoffs
                # ----------------------------------------------------------------------------------------------------
                if Constants.variation == 'lottery_hi':
                    lottery_hi = [cu(Constants.lottery_hi + (k - 1) * Constants.step_size) for k in indices]
                else:
                    lottery_hi = [cu(Constants.lottery_hi) for k in indices]

                # create list of low lottery payoffs
                # ----------------------------------------------------------------------------------------------------
                if Constants.variation == 'lottery_lo':
                    lottery_lo = [cu(Constants.lottery_lo - (k - 1) * Constants.step_size) for k in indices]
                else:
                    lottery_lo = [cu(Constants.lottery_lo) for k in indices]

                # create list of sure payoffs
                # ----------------------------------------------------------------------------------------------------
                if Constants.variation == 'sure_payoff':
                    sure_payoffs = [cu(Constants.sure_payoff + (k-1) * Constants.step_size) for k in indices]
                else:
                    sure_payoffs = [cu(Constants.sure_payoff) for k in indices]

                # create list of choices
                # ----------------------------------------------------------------------------------------------------
                p.participant.vars['cem_choices'] = list(
                    zip(
                        indices,
                        form_fields,
                        probabilities,
                        lottery_hi,
                        lottery_lo,
                        sure_payoffs
                    )
                )

                # randomly determine index/choice of binary decision to pay
                # ----------------------------------------------------------------------------------------------------
                p.participant.vars['cem_index_to_pay'] = random.choice(indices)
                p.participant.vars['cem_choice_to_pay'] = 'choice_' + str(p.participant.vars['cem_index_to_pay'])

                # randomize order of lotteries if <random_order = True>
                # ----------------------------------------------------------------------------------------------------
                if Constants.random_order:
                    random.shuffle(p.participant.vars['cem_choices'])

                # initiate list for choices made
                # ----------------------------------------------------------------------------------------------------
                p.participant.vars['cem_choices_made'] = [None for j in range(1, n + 1)]

            # generate random switching point for PlayerBot in tests.py
            # --------------------------------------------------------------------------------------------------------
            for participant in self.session.get_participants():
                participant.vars['cem-bot_switching_point'] = random.randint(1, n)


# ******************************************************************************************************************** #
# *** CLASS GROUP
# ******************************************************************************************************************** #
class Group(BaseGroup):
    pass


# ******************************************************************************************************************** #
# *** CLASS PLAYER
# ******************************************************************************************************************** #
class Player(BasePlayer):

    # add model fields to class player
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    for j in range(1, Constants.num_choices + 1):
        locals()['choice_' + str(j)] = models.StringField()
    del j

    random_draw = models.IntegerField()
    choice_to_pay = models.StringField()
    option_to_pay = models.StringField()
    inconsistent = models.IntegerField()
    switching_row = models.IntegerField()
    riskiness = models.IntegerField()
    confidence = models.IntegerField()

    # set player's payoff
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def set_payoffs(self):

        # random draw to determine whether to pay the "high" or "low" outcome of the randomly picked lottery
        # ------------------------------------------------------------------------------------------------------------
        self.random_draw = randrange(1, 100)

        # set <choice_to_pay> to participant.var['choice_to_pay'] determined creating_session
        # ------------------------------------------------------------------------------------------------------------
        self.choice_to_pay = self.participant.vars['cem_choice_to_pay']

        # determine whether the lottery (option "A") or the sure payoff (option "B") was chosen
        # ------------------------------------------------------------------------------------------------------------
        self.option_to_pay = getattr(self, self.choice_to_pay)

        # set player's payoff
        # ------------------------------------------------------------------------------------------------------------
        indices = [list(t) for t in zip(*self.participant.vars['cem_choices'])][0]
        index_to_pay = indices.index(self.participant.vars['cem_index_to_pay']) + 1
        choice_to_pay = self.participant.vars['cem_choices'][index_to_pay - 1]

        if self.option_to_pay == 'A':
            if self.random_draw <= choice_to_pay[2]:
                self.payoff = Constants.endowment + choice_to_pay[3]
            else:
                self.payoff = Constants.endowment + choice_to_pay[4]
        else:
            self.payoff = Constants.endowment + choice_to_pay[5]

        # set payoff as global variable
        # ------------------------------------------------------------------------------------------------------------
        self.participant.vars['cem_payoff'] = self.payoff
        self.participant.vars['cem_option_to_pay'] = self.option_to_pay

        # set payoff to zero if CEM is not the task to be payed
        # ------------------------------------------------------------------------------------------------------------
        if self.participant.vars['task_to_pay'] != 'cem':
            self.payoff = cu(0)

    # determine consistency
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def set_consistency(self):

        n = Constants.num_choices

        # replace A's by 1's and B's by 0's
        self.participant.vars['cem_choices_made'] = [
            1 if j == 'A' else 0 for j in self.participant.vars['cem_choices_made']
        ]

        # check for multiple switching behavior
        for j in range(1, n):
            choices = self.participant.vars['cem_choices_made']
            self.inconsistent = 1 if choices[j] > choices[j - 1] else 0
            if self.inconsistent == 1:
                break

    # determine switching row
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def set_switching_row(self):

        # set switching point to row number of first 'B' choice
        if self.inconsistent == 0:
            self.switching_row = sum(self.participant.vars['cem_choices_made']) + 1
