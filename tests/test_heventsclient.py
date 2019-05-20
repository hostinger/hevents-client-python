#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `hostinger_hevents`.`Event` module."""


import unittest

import xmlrunner
from requests import Request
from hostinger_hevents import HeventsClient


class TestHostingerHeventsHeventsClient(unittest.TestCase):
    """Tests for `hostinger_hevents`.`Event` module."""

    def setUp(self):
        self.api_urls = [
            'http://test.domain.com',
            'http://test.domain.com/'
        ]

    def tearDown(self):
        self.api_urls = None

    def test_can_use_hevents_endpoint(self):
        client = HeventsClient('http://test.domain.com', 'key')
        self.assertEqual(
            'http://test.domain.com',
            client.get_url()
        )

    def test_has_api_key_auth_header(self):
        client = HeventsClient('http://test.domain.com', 'key')
        self.assertIn(
            'Authorization',
            client.get_headers()
        )
        self.assertEqual(
            'Bearer key',
            client.get_headers()['Authorization']
        )

    def test_creates_post_request(self):
        client = HeventsClient('http://test.domain.com', 'key')
        request = client.create_request({'event': 'test', 'properties': {}})
        self.assertIsInstance(request, Request)
        self.assertTrue(request.method == 'POST')

    def test_creates_request_with_auth_header(self):
        client = HeventsClient('http://test.domain.com', 'key')
        request = client.create_request({'event': 'test', 'properties': {}})
        self.assertIn('Authorization', request.headers)
        self.assertTrue(request.headers['Authorization'])

    def test_can_get_url_with_endpoint(self):
        for uri in self.api_urls:
            client = HeventsClient(uri, 'key')
            self.assertRegex(
                client.get_full_url(),
                r'\/api\/events$'
            )


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)
