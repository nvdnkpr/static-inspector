# -*- coding: utf-8 -*-
import os
import unittest
from inspector.models.base import SourceFile


# TODO: test details!
from inspector.models.consts import Language


class TestJavaParse(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'java')

    def test_parse_1(self):
        sf = SourceFile.build_source_file(os.path.join(self.data_path, 'sample_sources', '1.java'))
        self.assertTrue(sf.language_detected)
        self.assertEqual(sf.language, Language.JAVA)
        self.assertTrue(sf.parsed)
        self.assertEqual(unicode(sf), u'Java SourceFile: 1 imports, 1 classes')
        self.assertEqual(sf.next_token(), None)
        c1 = sf.get_class('MyFirstProgram')
        self.assertEqual(c1.starting_line, 2)
        self.assertEqual(c1.ending_line, 23)
        self.assertEqual(len(c1.methods), 1)
        self.assertEqual(c1.get_method('main').line_count, 19)

    def test_parse_2(self):
        sf = SourceFile.build_source_file(os.path.join(self.data_path, 'sample_sources', '2.java'))
        self.assertEqual(unicode(sf), u'Java SourceFile: 1 classes')
        self.assertEqual(sf.get_class('Fibonacci').get_method('main').line_count, 11)
        self.assertEqual(sf.next_token(), None)

    def test_parse_3(self):
        sf = SourceFile.build_source_file(os.path.join(self.data_path, 'sample_sources', '3.java'))
        self.assertEqual(unicode(sf), u'Java SourceFile: 2 classes')
        self.assertEqual(sf.get_class('Point').get_method('clear').line_count, 5)
        self.assertEqual(sf.get_class('Pixel').get_method('clear').line_count, 4)
        self.assertEqual(sf.next_token(), None)

    def test_parse_4(self):
        sf = SourceFile.build_source_file(os.path.join(self.data_path, 'sample_sources', '4.java'))
        self.assertEqual(unicode(sf), u'Java SourceFile: 1 classes, 1 interfaces')
        self.assertEqual(sf.get_class('SimpleLookup').get_method('processValues').line_count, 7)
        self.assertEqual(sf.next_token(), None)

    def test_parse_5(self):
        sf = SourceFile.build_source_file(os.path.join(self.data_path, 'sample_sources', '5.java'))
        self.assertEqual(unicode(sf), u'Java SourceFile: 1 classes')
        mc = sf.get_class('PingPONG').get_method('PingPONG')
        self.assertEqual(mc.line_count, 4)
        self.assertTrue(mc.is_constructor())
        self.assertFalse(sf.get_class('PingPONG').get_method('run').is_constructor())
        self.assertEqual(sf.next_token(), None)

    def test_parse_6(self):
        sf = SourceFile.build_source_file(os.path.join(self.data_path, 'sample_sources', '6.java'))
        self.assertEqual(unicode(sf), u'Java SourceFile: 1 classes')
        account = sf.get_class('Account')
        self.assertEqual(len(account.methods), 4)
        self.assertEqual(len(account.fields), 1)
        self.assertEqual(account.get_method('abs').line_count, 8)
        self.assertEqual(sf.next_token(), None)


if __name__ == '__main__':
    unittest.main()
