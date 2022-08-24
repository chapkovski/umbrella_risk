from umbrella.configs.bret import Constants
from umbrella.payoff_setters import bret
import random



def get_form_fields(player):
    return  [
    'bret_bomb',
    'bret_boxes_collected',
    'bret_boxes_scheme',
    'bret_bomb_row',
    'bret_bomb_col',
]


def vars_for_template(player):
    reset = player.participant.vars.get('reset', False)
    if reset:
        del player.participant.vars['reset']
    input = not Constants.devils_game if not Constants.dynamic else False
    otree_vars = {
        'reset': reset,
        'input': input,
        'random': Constants.random,
        'dynamic': Constants.dynamic,
        'num_rows': Constants.num_rows,
        'num_cols': Constants.num_cols,
        'feedback': Constants.feedback,
        'undoable': Constants.undoable,
        'box_width': Constants.box_width,
        'box_height': Constants.box_height,
        'time_interval': Constants.time_interval,
    }
    return {
        'otree_vars': otree_vars,

    }

def before_next_page(player):
    player.participant.vars['reset'] = True
    bret.set_payoffs(player)



