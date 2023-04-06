from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from . import gamepages




class SecondPage(Page):
   pass


# print(getattr(gamepages, 'BretPage').template_name)
class _InnerTask(Page):
    num_task = None
    type = None

    def get_app(self):
        apps = self.participant.vars['appseq']
        return apps[self.num_task - 1]

    def get_template_names(self):
        app = self.get_app()
        if self.type == 'task':
            return [f'umbrella/tasks/{app}.html']
        if self.type == 'instructions':
            return [f'umbrella/instructions/{app}.html']
        return super().get_template_names()
    def _method_substitute(self, method):
        apps = self.participant.vars['appseq']
        app = apps[self.num_task - 1].lower()
        module = getattr(gamepages, app)
        return getattr(module, method)(self.player)

    def vars_for_template(self):
        return self._method_substitute('vars_for_template')

    def before_next_page(self):
        self._method_substitute('before_next_page')


class GeneralInstructions(_InnerTask):
    type = 'instructions'


class GeneralTask(_InnerTask):
    type = 'task'
    form_model = 'player'


    def get_form_fields(self):
        return self._method_substitute('get_form_fields')


class InstructionsP1(GeneralInstructions):
    num_task = 1


class P1(GeneralTask):
    num_task = 1


class InstructionsP2(GeneralInstructions):
    num_task = 2


class P2(GeneralTask):
    num_task = 2


class InstructionsP3(GeneralInstructions):
    num_task = 3


class P3(GeneralTask):
    num_task = 3


class InstructionsP4(GeneralInstructions):
    num_task = 4


class P4(GeneralTask):
    num_task = 4

class FirstPage(Page):
    pass

page_sequence = [
    # FirstPage,
    # SecondPage,
    InstructionsP1,
    P1,
    # InstructionsP2,
    P2,
    # InstructionsP3,
    P3,
    # InstructionsP4,
    P4
]
