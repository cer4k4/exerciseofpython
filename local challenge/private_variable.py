class Mapping:
    def __init__(self, iterable):
        self.items_list = []
        self.__update(iterable)

    def update(self, iterable):
        for item in iterable:
            self.items_list.append(item)
    __update = update   # private copy of original update() method

class MappingSubclass(Mapping):

    def update(self, keys, values):
        # provides new signature for update()
        # but does not break __init__()
        
        for item in {keys:values}:
            self.items_list.append(item)
        print(self._Mapping__update())

m = MappingSubclass("ali")
m.update("1","2")
#print(m.items_list)