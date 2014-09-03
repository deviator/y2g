#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest

from y2g import TableProcessor

class TableProcessorTestCase(unittest.TestCase):
    def setUp(self):
        self.processor = TableProcessor()

    def test_title_output_big(self):
        (t,e) = self.processor.titleOutput( "very " * self.processor.maxTitleLen + "big title" )
        self.assertTrue( len(e) > 0 )

    def test_title_output_small(self):
        (t,e) = self.processor.titleOutput( "small title" )
        self.assertTrue( len(e) == 0 )

    def test_text_output_big(self):
        (t1,t2,e) = self.processor.textOutput( "very " * self.processor.maxTextLen * 2 + "long text" )
        self.assertTrue( len(t1) < self.processor.maxTextLen )
        self.assertTrue( len(t2) > self.processor.maxTextLen )
        self.assertTrue( len(e) > 0 )

    def test_text_output_small(self):
        (t1,t2,e) = self.processor.textOutput( "very small text" )
        self.assertTrue( len(t1) < self.processor.maxTextLen )
        self.assertTrue( len(t2) < self.processor.maxTextLen )
        self.assertTrue( len(e) == 0 )

    def test_text_output_exclamation_eliminate(self):
        (t1,t2,e) = self.processor.textOutput( "many! exclamation! text!" )
        self.assertTrue( "!" not in t1 )
        self.assertTrue( "!" not in t2 )


if __name__ == '__main__':
    unittest.main()
