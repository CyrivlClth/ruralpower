from dataclasses import dataclass


@dataclass
class Admin(object):
    _id: str
    name: str
    mch_id: str
    mch_name: str

    def get_id(self):
        return self._id


def get_current_user():
    return Admin(_id='628d6233-14b7-4769-b1f7-1b3721227d57', name='admin',
                 mch_id='c5f66ffe-b9c4-49b8-8019-2a053f9d31a8', mch_name='2123')
