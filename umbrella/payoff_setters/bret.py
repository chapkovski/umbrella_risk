from umbrella.configs.bret import Constants
import random
from otree.api import BaseConstants, Currency as cu
def set_payoff(player):
    # determine round_result as (potential) payoff per round
    if player.bomb:
        player.payoff = cu(0)
    else:
        player.payoff = player.boxes_collected * Constants.box_value
    # set payoff and scheme as global variable
    # ------------------------------------------------------------------------------------------------------------
    player.participant.vars['bret_scheme'] = player.boxes_scheme
    player.participant.vars['bret_row'] = player.bomb_row
    player.participant.vars['bret_col'] = player.bomb_col
    player.participant.vars['bret_bomb'] = player.bomb
    player.participant.vars['bret_boxes'] = player.boxes_collected
    # set payoff and scheme as global variable
    # ------------------------------------------------------------------------------------------------------------
   # player.participant.vars['task_to_pay'] = 'bret'
    player.participant.vars['bret_payoff'] = player.payoff
    # set payoff to zero if BRET is not the task to be payed
    # ------------------------------------------------------------------------------------------------------------
    if player.participant.vars['task_to_pay'] != 'bret':
        player.payoff = cu(0)
