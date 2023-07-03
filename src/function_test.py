
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","web_monitor.settings")
django.setup()

from app.api_lib import apiLib
api_lib = apiLib()
api_lib.getLoginToken()