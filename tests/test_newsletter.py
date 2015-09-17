#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

"""
test_newsletter
----------------------------------

Tests for `newsletter` module.
"""

import unittest

from newsletter import newsletter
from collections import OrderedDict, Counter

class TestNewsletter(unittest.TestCase):

    def setUp(self):
        pass

    def test_count_args(self):
        template = """something {{one}}
                      other things {{two}} {{two}}"""

        results = newsletter.count_args(template)
        wanted = Counter({'one': 1, 'two': 2})

        self.assertEqual(results, wanted)

    def test_split_items(self):
        context = 'text1\n----\ntext2\n2nd line\n----\ntext3\n\n-----\ntext4'
        result = newsletter.split_items(context)
        wanted = ['text1', 'text2\n2nd line', 'text3', 'text4']
        self.assertEqual(result, wanted)

    def test_format_items(self):
        items = ['text1', 'text2']
        result = newsletter.format_items(items)
        wanted = "text1\n----\ntext2"
        self.assertEqual(result, wanted)

    def build_text(self):
        template = '\nTest\n{{one}}\ntest\n{{two}}\n{{two}}\n'
        arg2items = {'one': ['bob', 'alice'],
                     'two': ['kitty', 'bunny']}
        result = newsletter.build_text(template, arg2items)
        wanted = 'Test\nbob\ntest\nkitty\nbunny'
        self.assertEqual(result, wanted)

    def tearDown(self):
        pass
