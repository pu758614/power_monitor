
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","web_monitor.settings")
django.setup()

from app.lib.api_lib import apiLib
from app.lib.sync_data_lib import syncDataLib
import time

# syncDataLib().syncDevKpiDay()

r = syncDataLib().syncStationRealKpi()