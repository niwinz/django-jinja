# -*- coding: utf-8 -*-

from django.test import TestCase
from django_jinja.base import env

class TemplateFunctionsTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_template_filters(self):
        filters_data = [
            ("{{ 'test-1'|reverseurl }}", {}, '/test1/'),
            ("{{ 'test-1'|reverseurl(data=2) }}", {}, '/test1/2/'),
            ("{{ num|floatformat }}", {'num': 34.23234}, '34.2'),
            ("{{ num|floatformat(3) }}", {'num': 34.23234}, '34.232'),
        ]
        
        print

        for template_str, kwargs, result in filters_data:
            print "- Testing: ", template_str, "with:", kwargs

            template = env.from_string(template_str)
            _result = template.render(kwargs)
            self.assertEqual(_result, result)
