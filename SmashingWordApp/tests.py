import os
import sys
sys.path.append('/home/ubuntu/169proj/SmashingWord')
os.environ['DJANGO_SETTINGS_MODULE'] = "SmashingWord.settings"
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
