from umbrella.configs.cem import Constants
import random
from otree.api import BaseConstants, Currency as cu

def creating_session(self):
    print('CEM created')
    if self.round_number == 1:

        n = Constants.num_choices
        for p in self.get_players():

            # create list of lottery indices
            # ----------------------------------------------------------------------------------------------------
            indices = [j for j in range(1, n + 1)]

            # create list corresponding to form_field variables including all choices
            # ----------------------------------------------------------------------------------------------------
            form_fields = ['cem_choice_' + str(k) for k in indices]

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
                sure_payoffs = [cu(Constants.sure_payoff + (k - 1) * Constants.step_size) for k in indices]
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
            p.participant.vars['cem_choice_to_pay'] = 'cem_choice_' + str(p.participant.vars['cem_index_to_pay'])

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

