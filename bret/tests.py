# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import *
from otree.api import Bot



class PlayerBot(Bot):

    cases = ['always_bomb', 'never_bomb']

    def play_round(self):
        if Constants.instructions and self.player.round_number == 1:
            yield Instructions
        boxes_collected = 2
        yield (
            Decision,
           {
               'bomb_row': 1, 'bomb_col': 1, 'boxes_collected': boxes_collected,
               'bomb': 1 if self.case == 'always_bomb' else 0
           }
        )
        expected_round_result = 0 if self.case == 'always_bomb' else Constants.box_value * boxes_collected
        assert self.player.round_result == expected_round_result
        if Constants.results and self.player.round_number == Constants.num_rounds:
            # 1 round is chosen randomly
            assert self.participant.vars['bret_payoff'] == expected_round_result
            yield Results
