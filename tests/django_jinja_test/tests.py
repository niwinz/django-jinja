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
            ("{{ 'hola'|capfirst }}", {}, "Hola"),
            ("{{ 'hola mundo'|truncatechars(5) }}", {}, "ho..."),
            ("{{ 'hola mundo'|truncatewords(1) }}", {}, "hola ..."),
            ("{{ 'hola mundo'|truncatewords_html(1) }}", {}, "hola ..."),
            ("{{ 'hola mundo'|wordwrap(1) }}", {}, "hola\nmundo"),
            ("{{ 'hola mundo'|title }}", {}, "Hola Mundo"),
            ("{{ 'hola mundo'|slugify }}", {}, "hola-mundo"),
            ("{{ 'hello'|ljust(10) }}", {}, "hello     "),
            ("{{ 'hello'|rjust(10) }}", {}, "     hello"),
            ("{{ 'hello\nworld'|linebreaksbr }}", {}, "hello<br />world"),
        ]
        
        print
        for template_str, kwargs, result in filters_data:
            print "- Testing: ", template_str, "with:", kwargs

            template = env.from_string(template_str)
            _result = template.render(kwargs)
            self.assertEqual(_result, result)
