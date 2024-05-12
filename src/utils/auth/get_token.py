import os
import time
from datetime import datetime, timezone, timedelta

import jwt


def get_token(username: str) -> str:
    """
    Get token by username
    :param username:
    :return:
    """
    payload = {
        'user': username,
        'expires': (datetime.now(timezone.utc) + timedelta(minutes=15)).strftime('%m-%y-%d %H:%M:%S')
    }
    return jwt.encode(payload,
                      os.environ.get('JWT_SECRET', 'secret'),
                      algorithm='HS256')
