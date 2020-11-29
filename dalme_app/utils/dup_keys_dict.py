class DupKeyDict(dict):
    """ subclasses dict to create a dictionary that can
    contain duplicate keys (to support JSON conversion) """

    def __init__(self, items):
        self['foo'] = 'bar'
        self._items = items

    def items(self):
        return self._items
