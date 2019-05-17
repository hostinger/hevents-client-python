# -*- coding: utf-8 -*-
"""Hevents Client module."""

import logging

from requests import Request, PreparedRequest, Response, Session, utils
from requests.adapters import HTTPAdapter
from requests.exceptions import (HTTPError, RequestException,
                                 Timeout, TooManyRedirects)
from hostinger_hevents import Event


class HeventsClient:
    """Main class to crete Hevents Client."""

    def __init__(self, url: str, key: str):
        """Hevent Client constructor.

        Arguments:
            url {str} -- Where to send events to
            key {str} -- OAuth2.0 Bearer Authorization Token
        """
        self.url = None
        self.key = None
        self.client = None
        self.headers = dict()

        self.timeout = 10
        self.retries = 5

        self.logger = logging.getLogger(__name__)

        self.set_url(url)
        self.set_key(key)
        self.set_up_http_client_session(self.get_url())
        self.set_authorization_header(self.get_key())
        self.append_header('Content-Type', 'application/json')
        self.append_header('Accept', 'application/json')
        self.set_set_agent_header('Hostinger Hevents Client')

    def emit(self, event: dict, async_request: bool = False):
        """Emit provided event to the API Endpoint.

        Arguments:
            event {dict} -- Dict() representation of event data

            async_request {bool} -- If async should be used to send request
        """
        request = self.create_request(event)

        self.logger.info('Sending event URL: %s %s', request.url, request.json)
        if async_request:
            self.send_async(request)
        else:
            self.send(request)

    def set_up_http_client_session(self, url: str):
        """Mount requests.Session parameters to API Endpoint.

        Arguments:
            url {str} -- URL base to apply session parameters to
        """
        adapter = HTTPAdapter(max_retries=self.retries)
        self.session = Session()

        # Use `hevents_api_adapter` for all requests
        # to endpoints that start with this URL
        self.session.mount(url, adapter)

    def create_request(self, event: dict) -> PreparedRequest:
        """Create Request object that will be sent later.

        Arguments:
            event {dict}

        Returns:
            Request -- requests.Request objects
        """
        return Request(
            'POST',
            self.get_full_url(),
            json=Event.from_dict(event).as_dict(),
            headers=self.get_headers()
        )

    def send(self, request: Request) -> Response:
        """Send crafted request to API.

        Arguments:
            request {Request} -- Request object to work on

        Returns:
            Response -- requests.Response object
        """
        with self.session as sess:
            prepared_request = sess.prepare_request(request)
            try:
                response = sess.send(prepared_request,)
            except (ConnectionError, HTTPError, Timeout, TooManyRedirects, RequestException) as err:
                self.logger.error('Request error: %s', err)
                return
        if response.history:
            for resp in response.history:
                self.logger.info('Request was redirected: %d %s', resp.status_code, resp.url)
            self.logger.info('Final destination: %d %s', response.status_code, response.url)

        self.logger.info('Got response: [%d] %s', response.status_code, response.text)

    def send_async(self, request: Request):
        """Send crafted request to API.

        Arguments:
            request {Request} -- Request object to work on

        Raises:
            NotImplementedError: This function is NOT implemented yet
        """
        raise NotImplementedError

    def set_authorization_header(self, key: str):
        """Set 'Authorization' header.

        Arguments:
            key {str}
        """
        self.append_header('Authorization', key)

    def set_set_agent_header(self, prefix: str):
        """Set 'User-Agent' header.

        Arguments:
            prefix {str} -- Prefix should identify this library
        """
        self.append_header(
            'User-Agent',
            f"{prefix} {utils.default_user_agent()}"
        )

    def append_header(self, header: str, value: str):
        """Append headers to use with request to API.

        Arguments:
            header {str} -- Header name

            value {str} -- Header value
        """
        self.headers[header] = value

    def get_headers(self) -> dict:
        """Get all of the headers set at present time.

        Returns:
            dict -- Request headers
        """
        return self.headers

    def get_url(self) -> str:
        """Get API URL address.

        Returns:
            str -- API location
        """
        return self.url

    def set_url(self, url: str):
        """Set API URL address.

        Arguments:
            url {str} -- API location
        """
        self.url = url

    def get_key(self) -> str:
        """Get Authorization key for API.

        Returns:
            str -- Authorization key
        """
        return f"Bearer {self.key}"

    def set_key(self, key: str):
        """Set Authorization key for API.

        Arguments:
            key {str} -- Authorization key
        """
        self.key = key

    def get_full_url(self) -> str:
        """Get full URL to API Endpoint.

        Returns:
            str -- Full path to API endpoint
        """
        url = self.get_url().rstrip('/')
        uri = self.get_endpoint().rstrip('/')

        return f"{url}/{uri}"

    @staticmethod
    def get_endpoint() -> str:
        """Get API Endpoint.

        Returns:
            str -- URI part of API Endpoint
        """
        return 'api/events'
