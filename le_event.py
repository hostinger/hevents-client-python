"""Something."""

from hostinger_hevents import HeventsClient

event = {
    'event': 'USER_SIGN_UP',
    'properties': {
        'user_id': 123,
        'time': '2020-02-02',
        'details': {
            'email': 'ex@ample.com',
            'name': 'Hevents'
        }
    }
}

client = HeventsClient('https://hevents.hostinger.ioz', 'zZdAjIMMML62XWrtiNYNreNLaO5MX1bpjqeTyUa8miZ4qLGAhXeRx8McaGID');
response = client.emit(event)
