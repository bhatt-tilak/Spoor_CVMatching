### apps.py lists the name of all apps int the project
## an app or application is a specific part of project
# used for modular development


from django.apps import AppConfig


class UiConfig(AppConfig):
    name = 'UI'
