from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class _InnerTask(Page):
    pass


class GeneralInstructions(_InnerTask):
    pass


class GeneralTask(_InnerTask):
    pass


class InstructionsP1(GeneralInstructions):
    pass


class P1(GeneralTask):
    pass


class InstructionsP2(GeneralInstructions):
    pass


class P2(GeneralTask):
    pass


class InstructionsP3(GeneralInstructions):
    pass


class P3(GeneralTask):
    pass


class InstructionsP4(GeneralInstructions):
    pass


class P4(GeneralTask):
    pass


page_sequence = [
    InstructionsP1,
    P1,
    InstructionsP2,
    P2,
    InstructionsP3,
    P3,
    InstructionsP4,
    P4
]
