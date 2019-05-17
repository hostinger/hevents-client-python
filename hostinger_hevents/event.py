# -*- coding: utf-8 -*-
"""Event module."""

from collections import defaultdict


class Event:
    """Main class to define, verify, and emit events."""

    def __init__(self, name: str, properties: dict):
        """Event constructor.

        Arguments:
            name {str} -- Event name
            properties {dict} -- Event properties
        """
        self.name = name
        self.properties = properties

    def as_dict(self) -> str:
        """String representation of Event object.

        Returns:
            str -- String representation of the Event instance
        """
        return {
            'event': self.get_name(),
            'properties': self.get_properties()
        }

    @staticmethod
    def from_dict(params: dict):
        """Create Event from the passed dict.

        Arguments:
            params {dict} -- Event parameters

        Returns:
            Event -- Event instance having provided event parameters
        """
        Event.validate(Event.expected_args(), params)
        return Event(params['event'], params['properties'])

    @staticmethod
    def validate(expected: dict, received: dict):
        """Validate event structure, fields, and field types.

        Arguments:
            expected {dict} -- Expected event properties

            received {dict} -- Received event properties

        Raises:
            NameError: If expected event parameter is not passed

            ValueError: If received event parameter has wrong value type
        """
        for expected_arg, expected_value in expected.items():
            if expected_arg not in received and 'default' in expected_value:
                received[expected_arg] = expected_value['default']

            if expected_value['required'] and expected_arg not in received:
                raise NameError(
                    f"Required argument `{expected_arg}` is missing"
                )

            received_type = type(received[expected_arg]).__name__
            if received_type != expected_value['type']:
                raise ValueError(
                    f"Argument `{expected_arg}` is expected to be of type "
                    f"`{expected_value['type']}`, received `{received_type}`"
                )

    @staticmethod
    def expected_args() -> dict:
        """Define expected event schema, field, and types.

        Returns:
            dict -- Event schema description
        """
        args = defaultdict()
        args = {
            'event': {
                'type': 'str',
                'required': True
            },
            'properties': {
                'type': 'dict',
                'required': True,
                'default': {}
            }
        }
        return args

    def get_name(self) -> str:
        """Get Event name.

        Returns:
            str -- Event name
        """
        return self.name

    def set_name(self, name: str):
        """Set Event name.

        Arguments:
            name {str} -- Event name
        """
        self.name = name

    def get_properties(self) -> dict:
        """Get Event properties.

        Returns:
            dict -- Event properties
        """
        return self.properties

    def set_properties(self, properties: dict):
        """Set Event properties.

        Arguments:
            properties {dict} -- Event properties
        """
        self.properties = properties
