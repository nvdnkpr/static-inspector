# -*- coding: utf-8 -*-
import os
import unittest

from inspector.models.base import Comment, Project


class BaseModelTest(unittest.TestCase):
    def test_comment(self):
        c1 = Comment(u'// comment 1')
        self.assertEqual(c1.content, u'comment 1')
        self.assertFalse(c1.doc_comment)
        self.assertFalse(c1.multiline)
        self.assertEqual(unicode(c1), u'Comment: comment 1')
        self.assertEqual(str(c1), 'Comment: comment 1')

        c2 = Comment(u'/*******************\n * Comment2 _ \n****/')
        self.assertEqual(c2.content, u'Comment2 _')
        self.assertTrue(c2.doc_comment)
        self.assertTrue(c2.multiline)
        self.assertEqual(unicode(c2), u'Comment: Comment2 _ (docstring)')

        self.assertRaises(ValueError, Comment, u'int x = 2;')

    def test_project_dfs_files(self):
        class TestFileDfsHandler(Project.FileDfsHandler):
            def __init__(self):
                super(TestFileDfsHandler, self).__init__()
                self.files = []
                self.dir_xml = ''

            def handle_file(self, path):
                self.files.append(path)

            def normalize_path(self, path):
                return path.replace('/', '.').replace('\\', '.')

            def enter_dir(self, path):
                self.dir_xml += u'<{0}>'.format(self.normalize_path(path))

            def exit_dir(self, path):
                self.dir_xml += u'</{0}>'.format(self.normalize_path(path))

        tests_path = os.path.abspath(os.path.dirname(__file__))
        p = Project(tests_path)
        p.ignored_dirs.append('__pycache__')
        p.ignored_dirs.append('data/android')
        hnd = TestFileDfsHandler()
        p.dfs_files(hnd)
        self.assertGreaterEqual(len(hnd.files), 11)  # counting possible pyc/... files
        self.assertIn('model_test.py', hnd.files)
        for i in range(1, 7):
            self.assertIn('data/java/sample_sources/{0}.java'.format(i), hnd.files)
        DIRS = u'<><data><data.java><data.java.sample_sources></data.java.sample_sources></data.java></data></>'
        self.assertEqual(hnd.dir_xml, DIRS)


if __name__ == '__main__':
    unittest.main()
