import sys
import os
import django

sys.path.append('spread')
os.environ['DJANGO_SETTINGS_MODULE'] = 'spread.settings'
django.setup()

from django.utils import timezone
today = timezone.now()
print(today.date())