from .sharify_object import SharifyObject


class Health(SharifyObject):
    def __init__(self, status):
        self.status = status
