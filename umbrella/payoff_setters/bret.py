from umbrella.configs.bret import Constants
import random
from otree.api import BaseConstants, Currency as cu
def set_payoffs(player):
    # determine round_result as (potential) payoff per round
    if player.bret_bomb:
        player.bret_payoff = cu(0)
    else:
        player.bret_payoff = player.bret_boxes_collected * Constants.box_value
    # set payoff and scheme as global variable
    # ------------------------------------------------------------------------------------------------------------
    player.participant.vars['bret_scheme'] = player.bret_boxes_scheme
    player.participant.vars['bret_row'] = player.bret_bomb_row
    player.participant.vars['bret_col'] = player.bret_bomb_col
    player.participant.vars['bret_bomb'] = player.bret_bomb
    player.participant.vars['bret_boxes'] = player.bret_boxes_collected
    player.participant.vars['bret_payoff'] = player.bret_payoff
