from umbrella.configs.mpl import Constants
import random
from otree.api import BaseConstants, Currency as cu


def creating_session(self):
    print('MPL created')
    if self.round_number == 1:

        n = Constants.num_choices
        for p in self.get_players():

            # create list of lottery indices
            # ----------------------------------------------------------------------------------------------------
            indices = [j for j in range(1, n)]
            indices.append(n) if Constants.certain_choice else None

            # create list of probabilities
            # ----------------------------------------------------------------------------------------------------
            if Constants.percentage:
                probabilities = [
                    "{0:.2f}".format(k / n * 100) + "%"
                    for k in indices
                ]
            else:
                probabilities = [
                    str(k) + "/" + str(n)
                    for k in indices
                ]

            # create list corresponding to form_field variables including all choices
            # ----------------------------------------------------------------------------------------------------
            form_fields = ['mpl_choice_' + str(k) for k in indices]

            # create list of choices
            # ----------------------------------------------------------------------------------------------------
            p.participant.vars['mpl_choices'] = list(
                zip(indices, form_fields, probabilities)
            )

            # randomly determine index/choice of binary decision to pay
            # ----------------------------------------------------------------------------------------------------
            p.participant.vars['mpl_index_to_pay'] = random.choice(indices)
            p.participant.vars['mpl_choice_to_pay'] = 'mpl_choice_' + str(p.participant.vars['mpl_index_to_pay'])

            # randomize order of lotteries if <random_order = True>
            # ----------------------------------------------------------------------------------------------------
            if Constants.random_order:
                random.shuffle(p.participant.vars['mpl_choices'])

            # initiate list for choices made
            # ----------------------------------------------------------------------------------------------------
            p.participant.vars['mpl_choices_made'] = [None for j in range(1, n + 1)]

        # generate random switching point for PlayerBot in tests.py
        # --------------------------------------------------------------------------------------------------------
        for participant in self.session.get_participants():
            participant.vars['mpl_switching_point'] = random.randint(1, n)

