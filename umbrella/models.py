from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from .configs.cem import Constants as CEM_Constants
from .configs.mpl import Constants as MPL_Constants
import random
import json
import itertools
from umbrella import session_creator

author = "Philipp Chapkovski, WZB"

doc = """
Umbrella app for several risk measures
"""


class Constants(BaseConstants):
    name_in_url = "umbrella"
    players_per_group = None
    num_rounds = 2
    control_win = 5
    risk_win = 10
    TREATMENTS = ["risk", "ambiguity", "control"]
    TREATMENTS = [
        dict(name="T1-CC", treatments=["control", "control"]),
        dict(name="T2-CR", treatments=["control", "risk"]),
        dict(name="T3-CA", treatments=["control", "ambiguity"]),
        dict(name="T4-RA", treatments=["risk", "ambiguity"]),
        dict(name="T5-AR", treatments=["ambiguity", "risk"]),
        dict(name="T6-RC", treatments=["risk", "control"]),
        dict(name="T7-AC", treatments=["ambiguity", "control"]),
    ]
    APPS = [  "CEM", "MPL", "SCL"]
    treatment_correspodence = dict(
        control=dict(cover=False, risk=lambda x: 100),
        risk=dict(cover=False, risk=lambda x: x.session.config.get("risk", 50)),
        ambiguity=dict(cover=True, risk=lambda x: random.choice(range(0, 101, 10))),
    )


class Subsession(BaseSubsession):
    def bret_creating_session(self):
        pass

    def creating_session(self):
        # session_creator.bret.creating_session(self)
        session_creator.cem.creating_session(self)
        session_creator.mpl.creating_session(self)
        session_creator.scl.creating_session(self)

        if self.round_number == 1:
            len_treat_comb = len(Constants.TREATMENTS)
            for i, p in enumerate(self.session.get_participants()):
                _id = i % len_treat_comb
                p.vars["treatment_set"] = Constants.TREATMENTS[_id]

                p.vars["treatments"] = p.vars["treatment_set"]["treatments"]
                apps = Constants.APPS.copy()
                random.shuffle(apps)
                p.vars["appseq"] = apps
                p.vars["payable_app"] = random.choice(apps)
                p.vars["payable_task_num"] = apps.index(p.vars["payable_app"]) + 1
                # p.vars['payable_round'] = random.randint(1, Constants.num_rounds)
                p.vars[
                    "payable_round"
                ] = 1  # TODO!!!! NB!!!! remove - just for deebugging
                p.vars["lottery_outcome"] = random.uniform(0, 360)

        for p in self.get_players():
            p.glob_treatment=p.participant.vars['treatment_set']['name']
            p.treatment = p.participant.vars["treatments"][self.round_number - 1]
            p.appseq = json.dumps(p.participant.vars["appseq"])
            treatment_params = Constants.treatment_correspodence[p.treatment]
            p.risk = treatment_params.get("risk")(p)
            p.cover = treatment_params.get("cover")
            p.payable_app = p.participant.vars.get("payable_app")
            p.payable_task_num = p.participant.vars.get("payable_task_num")
            p.payable_round = p.participant.vars.get("payable_round")
            p.lottery_outcome = p.participant.vars.get("lottery_outcome")
            p.bin_lottery_outcome = p.lottery_outcome >= 360 * (1 - p.risk / 100)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def set_final_payoffs(self):
        p = self
        payable_player = p.in_round(p.payable_round)
        payable_app = payable_player.payable_app
        self.felix_payoff = getattr(self, f"{payable_app.lower()}_payoff")
        if p.payable_treatment == "control":
            base_payoff = Constants.control_win
        else:
            base_payoff = Constants.risk_win
        self.background_payoff = p.payable_bin_lottery_outcome * base_payoff

        self.payoff = self.background_payoff + self.felix_payoff

    def start(self):
        p = self
        payable_player = p.in_round(p.payable_round)

        p.payable_risk = payable_player.risk
        p.payable_lottery_outcome = payable_player.lottery_outcome
        p.payable_bin_lottery_outcome = payable_player.bin_lottery_outcome
        p.payable_treatment = payable_player.treatment

    glob_treatment = models.StringField()
    bret_payoff = models.CurrencyField()
    cem_payoff = models.CurrencyField()
    mpl_payoff = models.CurrencyField()
    scl_payoff = models.CurrencyField()
    consent = models.BooleanField(
        widget=widgets.CheckboxInput, label="I have read this consent form and I agree"
    )
    treatment = models.StringField()
    appseq = models.StringField()
    cover = models.BooleanField()
    risk = models.IntegerField()
    payable_round = models.IntegerField()
    payable_app = models.StringField()
    payable_task_num = models.IntegerField()
    payable_risk = models.IntegerField()
    payable_lottery_outcome = models.FloatField()
    payable_bin_lottery_outcome = models.BooleanField()
    payable_treatment = models.StringField()
    lottery_outcome = models.FloatField()
    bin_lottery_outcome = models.BooleanField()
    background_payoff = models.CurrencyField()
    felix_payoff = models.CurrencyField()

    def get_apps(self):
        return self.participant.vars["appseq"]

    ##############################BRET###############################
    bret_bomb = models.IntegerField()
    bret_bomb_row = models.PositiveIntegerField()
    bret_bomb_col = models.PositiveIntegerField()
    bret_boxes_collected = models.IntegerField()
    bret_boxes_scheme = models.StringField()

    ##############################END OF BRET###############################
    ##############################CEM###############################
    # add model fields to class player
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    for j in range(1, CEM_Constants.num_choices + 1):
        locals()["cem_choice_" + str(j)] = models.StringField()
    del j

    cem_random_draw = models.IntegerField()
    cem_choice_to_pay = models.StringField()
    cem_option_to_pay = models.StringField()
    cem_inconsistent = models.IntegerField()
    cem_switching_row = models.IntegerField()

    ##############################END OF CEM###############################

    ##############################SCL###############################
    # add model fields to class player
    # ----------------------------------------------------------------------------------------------------------------
    scl_lottery_choice = models.IntegerField()
    scl_outcome_to_pay = models.StringField()
    ##############################END OF SCL###############################

    ##############################MPL###############################

    for j in range(1, MPL_Constants.num_choices + 1):
        locals()["mpl_choice_" + str(j)] = models.StringField()
    del j

    mpl_random_draw = models.IntegerField()
    mpl_choice_to_pay = models.StringField()
    mpl_option_to_pay = models.StringField()
    mpl_inconsistent = models.IntegerField()
    mpl_switching_row = models.IntegerField()

    ##############################END OF MPL###############################

    ##############################QUIZES###############################
    cq_1 = models.StringField(
        label="At the end of the study, how many decisions will be paid out?",
        choices=[str(i) for i in range(1, 13)],
        widget=widgets.RadioSelect,
    )
    cq_2 = models.StringField(
        label="Does the decision in one part of the experiment influence the outcome of other parts?",
        choices=["Yes", "No"],
        widget=widgets.RadioSelect,
    )
    cq_control = models.StringField(
        label=" How likely is it, that you receive an additional 5€?",
        choices=[f"{i}%" for i in range(0, 101, 10)] + ["I do not know"],
        widget=widgets.RadioSelect,
    )
    cq_risk = models.StringField(
        label="How likely is it, that you receive an additional 10€?",
        choices=[f"{i}%" for i in range(0, 101, 10)] + ["I do not know"],
        widget=widgets.RadioSelect,
    )
    cq_ambiguity = models.StringField(
        label="How likely is it, that you receive an additional 10€?",
        choices=[f"{i}%" for i in range(0, 101, 10)] + ["I do not know"],
        widget=widgets.RadioSelect,
    )
    ##############################END OF MPL###############################
