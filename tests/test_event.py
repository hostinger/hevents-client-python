#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `hostinger_hevents`.`Event` module."""


import unittest

import xmlrunner
from hostinger_hevents import Event


class TestHostingerHeventsEvent(unittest.TestCase):
    """Tests for `hostinger_hevents`.`Event` module."""

    def setUp(self):
        self.invalid_events = [
            {'event': True, 'properties': {'test_prop': 'test_value'}},
            {'properties': {'test_prop': 'test_value'}},
            {'event': True, 'properties': 'test_prop'}
        ]

    def tearDown(self):
        self.invalid_events = None

    def test_can_get_name(self):
        event = Event('test_event', {'test_prop': 'test_value'})
        self.assertEqual(
            'test_event',
            event.get_name()
        )

    def test_can_set_name(self):
        event = Event('test_name', {'test_prop': 'test_value'})
        event.set_name('test_name2')
        self.assertEqual(
            'test_name2',
            event.get_name()
        )

    def test_can_get_properties(self):
        event = Event('test_name', {'test_prop': 'test_value'})
        self.assertEqual(
            {'test_prop': 'test_value'},
            event.get_properties()
        )

    def test_can_set_properties(self):
        event = Event('test_name', {'test_prop': 'test_value'})
        event.set_properties({'test_prop2': 'test_value2'})
        self.assertEqual(
            {'test_prop2': 'test_value2'},
            event.get_properties()
        )

    def test_can_get_json(self):
        event = Event('test_name', {'test_prop': 'test_value'})
        self.assertEqual(
            {"event": "test_name", "properties": {"test_prop": "test_value"}},
            event.as_dict()
        )

    def test_can_create_from_dict(self):
        event = Event.from_dict(
            {
                'event': 'test_name',
                'properties': {
                    'test_prop': 'test_value'
                }
            }
        )
        self.assertIsInstance(event, Event)

    def test_creates_without_properties(self):
        event = Event.from_dict({'event': 'test_name'})
        self.assertTrue(event.get_properties() == {})

    def test_fails_with_invalid_event_arguments(self):
        for event in self.invalid_events:
            with self.assertRaises((ValueError, NameError)):
                Event.from_dict(event)

    def test_can_get_string_from_dict(self):
        event = Event.from_dict(
            {
                'event': 'test_name',
                'properties': {
                    'test_prop': 'test_value'
                }
            }
        )
        self.assertEqual(
            {"event": "test_name", "properties": {"test_prop": "test_value"}},
            event.as_dict()
        )

if __name__ == '__main__':  # pylint: disable=R0801
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)
