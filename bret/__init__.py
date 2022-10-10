import random

from otree.api import *

from .config import Constants
import json
from StartApp.pages import Page


author = 'Felix Holzmeister & Armin Pfurtscheller'
doc = """
Bomb Risk Elicitation Task (BRET) à la Crosetto/Filippin (2013), Journal of Risk and Uncertainty (47): 31-65.
"""
# ******************************************************************************************************************** #
# *** CLASS SUBSESSION *** #
# ******************************************************************************************************************** #
class Subsession(BaseSubsession):
    pass


# ******************************************************************************************************************** #
# *** CLASS GROUP *** #
# ******************************************************************************************************************** #
class Group(BaseGroup):
    pass


# ******************************************************************************************************************** #
# *** CLASS PLAYER *** #
# ******************************************************************************************************************** #
class Player(BasePlayer):
    bomb = models.IntegerField()
    bomb_row = models.PositiveIntegerField()
    bomb_col = models.PositiveIntegerField()
    boxes_collected = models.IntegerField()
    boxes_scheme = models.StringField()
    riskiness = models.IntegerField(
        choices = [
            [1,'Low'],
            [2],
            [3],
            [4],
            [5],
            [6],
            [7, 'high']]
    )
    confidence = models.IntegerField(
        choices = [
            [1,'Low'],
            [2],
            [3],
            [4],
            [5],
            [6],
            [7, 'high']]
    )


# FUNCTIONS
def set_payoff(player: Player):
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


# PAGES
# ******************************************************************************************************************** #
# *** CLASS INSTRUCTIONS *** #
# ******************************************************************************************************************** #
class Instructions(Page):
    template_name = 'bret/templates/Instructions.html'
    # only display instruction in round 1
    
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1

    # variables for use in template
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'num_rows': Constants.num_rows,
            'num_cols': Constants.num_cols,
            'num_boxes': Constants.num_rows * Constants.num_cols,
            'num_nobomb': Constants.num_rows * Constants.num_cols - 1,
            'box_value': Constants.box_value,
            'time_interval': Constants.time_interval,
            'task_number': player.participant.vars['task_number'] 
        }


# ******************************************************************************************************************** #
# *** CLASS BOMB RISK ELICITATION TASK *** #
# ******************************************************************************************************************** #
class Decision(Page):
    # form fields on player level
    template_name = 'bret/templates/Decision.html'
    form_model = 'player'
    form_fields = [
        'bomb',
        'boxes_collected',
        'boxes_scheme',
        'bomb_row',
        'bomb_col',
    ]
    # jsonify BRET settings for Javascript application
    @staticmethod
    def vars_for_template(player: Player):
        reset = player.participant.vars.get('reset', False)
        if reset == True:
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
            'task_number': player.participant.vars['task_number'] 
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['reset'] = True
        set_payoff(player)
        player.participant.vars['task_number'] = player.participant.vars['task_number']+1

    # @staticmethod
    # def app_after_this_page(player, upcoming_apps):
    #     if player.whatever:
    #         return upcoming_apps[0]


# ******************************************************************************************************************** #
# *** CLASS SURVEY *** #
# ******************************************************************************************************************** #
class Survey(Page):

    # form fields on player level
    form_model = 'player'
    form_fields = ['riskiness', 'confidence']
    # variables for use in template
    template_name = 'bret/templates/Survey.html'
    @staticmethod
    def vars_for_template(player: Player):
        state = {
            "bomb": {
                "row": player.participant.vars['bret_row'],
                "col": player.participant.vars['bret_col'],
            },
            "collection": json.loads(player.participant.vars['bret_scheme']),
            "started": True,
            "stopped": True,
            "resolved": False,
        }
        reset = player.participant.vars.get('reset', False)
        if reset == True:
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
            'bret_state': state,
        }
        return {'otree_vars': otree_vars}


# ******************************************************************************************************************** #
# *** PAGE SEQUENCE *** #
# ******************************************************************************************************************** #
page_sequence = [Decision,
#Survey
]
if Constants.instructions:
    page_sequence.insert(0, Instructions)
