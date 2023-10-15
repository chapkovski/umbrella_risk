from os import environ

app_seq = [

    'umbrella',
    'q',

]
SESSION_CONFIGS = [
    dict(
        name='q',
        display_name="Post-experimental questionnaire only",
        num_demo_participants=1,
        app_sequence=['q'],

    ),
    dict(
        name='umbrella',
        #    display_name="Control",
        num_demo_participants=14,
        app_sequence=app_seq,

    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    prolific_return_url="https://app.prolific.com/submissions/complete?cc=NO_CODE",
    for_prolific=True,
    real_world_currency_per_point=1.00, participation_fee=0, doc="",
    risk=50
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'y0wk^6j@f=kavhihmw9s@7o#j)69(_rid=83ghba8j4o(i$wel'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
POINTS_DECIMAL_PLACES = 2
