# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2017-2019 by the contributors (see AUTHORS file).
    :license: BSD-2-Clause, see LICENSE for details.
"""

from sphinxcontrib.confluencebuilder.state import ConfluenceState
from sphinxcontrib_confluencebuilder_util import ConfluenceTestUtil as _
from sphinxcontrib.confluencebuilder.builder import ConfluenceBuilder
import os
import re
import unittest
import tempfile
import shutil


class TestImageStar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_dir = os.path.dirname(os.path.realpath(__file__))
        cls.image_file = os.path.join(cls.test_dir, 'assets', 'image01.png')

    def build_document_given_dataset(self, dataset):
        config = _.prepareConfiguration()
        doc_dir, doctree_dir = _.prepareDirectories('image-star')
        _.buildSphinx(dataset, doc_dir, doctree_dir, config)
        return doc_dir

    def test_all_supported_extensions(self):
        ''' For every supported extension by the Builder
        a temporary sourcesdir is created with the original index.rst
        and a link to the original image file. The link name will end
        with the tested extension. Then we build the document.
        '''
        dataset = os.path.join(self.test_dir, 'dataset-image-star')
        image_basename = os.path.basename(self.image_file).split('.')[0]
        for image_type in ConfluenceBuilder.supported_image_types:
            specifig_dataset = tempfile.mkdtemp()
            extension = re.sub(r'.*/', '', image_type)
            os.symlink(os.path.join(dataset, 'index.rst'),
                       os.path.join(specifig_dataset, 'index.rst'))
            os.symlink(self.image_file,
                       os.path.join(specifig_dataset,
                                    image_basename + '.' + extension))
            doc_dir = self.build_document_given_dataset(specifig_dataset)
            expected = os.path.join(self.test_dir, 'expected-image-star')
            _.assertExpectedWithOutput(
                self, 'index', expected, doc_dir)
            shutil.rmtree(specifig_dataset)
