import os
import time

import jwt


def get_token(username: str) -> str:
    payload = {
        'user': username,
        'expires': time.time() + 3600
    }
    return jwt.encode(payload,
                      os.environ.get('JWT_SECRET', 'secret'),
                      algorithm='HS256')
