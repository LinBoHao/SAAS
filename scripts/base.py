# -*- coding:utf-8 -*-

import os
import django
import sys


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SAAS.settings")
django.setup()
