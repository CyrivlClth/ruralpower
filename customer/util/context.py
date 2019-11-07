from dataclasses import dataclass


@dataclass
class User(object):
    _id: str
    name: str
    mobile: str

    def get_id(self):
        return self._id


def get_current_user():
    return User(_id='628d6233-14b7-4769-b1f7-1b3721227d57', name='admin', mobile='2123')
