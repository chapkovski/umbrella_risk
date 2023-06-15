from otree.api import Currency as c, currency_range
from ._builtin import Page as oTreePage, WaitPage
from .models import Constants
from . import gamepages

SECTIONS = ["Instructions", "Part 1", "Part 2", "Final part"]


class Page(oTreePage):
    instructions = False
    active_section = None

    def get_context_data(self, **context):
        r = super().get_context_data(**context)
        r["maxpages"] = self.participant._max_page_index
        r["page_index"] = self._index_in_pages
        r[
            "progress"
        ] = f"{int(self._index_in_pages / self.participant._max_page_index * 100):d}"
        r["instructions"] = self.instructions
        r["sections"] = [
            dict(name=i, active="active" if i == self.active_section else "")
            for i in SECTIONS
        ]
        return r


class SecondPage(Page):
    active_section = "Instructions"
    pass


# print(getattr(gamepages, 'BretPage').template_name)
class _InnerTask(Page):
    num_task = None
    type = None

    def get_app(self):
        apps = self.participant.vars["appseq"]
        return apps[self.num_task - 1]

    def get_template_names(self):
        app = self.get_app()
        if self.type == "task":
            return [f"umbrella/tasks/{app}.html"]
        if self.type == "instructions":
            return [f"umbrella/instructions/{app}.html"]
        return super().get_template_names()

    def _method_substitute(self, method):
        apps = self.participant.vars["appseq"]
        app = apps[self.num_task - 1].lower()
        module = getattr(gamepages, app)
        return getattr(module, method)(self.player)

    def vars_for_template(self):
        return self._method_substitute("vars_for_template")

    def before_next_page(self):
        if self.type == "task":
            self._method_substitute("before_next_page")


class GeneralInstructions(_InnerTask):
    type = "instructions"


class GeneralTask(_InnerTask):
    type = "task"
    form_model = "player"
    instructions = True

    def instructions_path(self):
        app = self.get_app()
        return f"umbrella/instructions/inner_{app}.html"

    def get_form_fields(self):
        return self._method_substitute("get_form_fields")


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


class ConsentPage(Page):
    active_section = "Instructions"
    form_fields = ["consent"]
    form_model = "player"

    def is_displayed(self):
        return self.round_number == 1


class OverallInstructions(Page):
    active_section = "Instructions"
    form_fields = ["consent"]
    form_model = "player"

    def is_displayed(self):
        return self.round_number == 1


class FirstPage(Page):
    

    def vars_for_template(self):
        return dict(no_risk_perc=100 - self.player.risk)


class OverallQuiz(Page):
    active_section = "Instructions"
    instructions = True
    instructions_path = "umbrella/instructions/overall.html"
    form_model = "player"
    form_fields = ["cq_1", "cq_2"]

    def is_displayed(self):
        return self.round_number == 1


class QuizForTreatment(Page):
    instructions = True

    def instructions_path(self):
        return f"umbrella/instructions/{self.player.treatment}.html"

    form_model = "player"

    def get_form_fields(self):
        return [f"cq_{self.player.treatment}"]


class LotteryResults(Page):
    def vars_for_template(self):
        # TODO: it's stupid but for now let's do it right here for debuggin reasons.
        # TODO: let's move it later to P4's BNP
        self.player.set_final_payoffs()
        return {}

    pass
    # def is_displayed(self):
    #     return self.round_number == Constants.num_rounds


page_sequence = [
    ConsentPage,
    OverallInstructions,
    OverallQuiz,
    FirstPage,
    SecondPage,
    QuizForTreatment,
    InstructionsP1,
    P1,
    InstructionsP2,
    P2,
    InstructionsP3,
    P3,
    InstructionsP4,
    P4,
    LotteryResults,
]
