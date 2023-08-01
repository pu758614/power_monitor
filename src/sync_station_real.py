
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","web_monitor.settings")
django.setup()

from app.lib.sync_data_lib import syncDataLib

r = syncDataLib().syncStationRealKpi()