
"""
    Stub implementation of mock redis cache / db
    Limitations (not a complete list):
      - smembers are all stored in one array
      - incr just increments one variable
"""

class Redis():

    def __init__(self):
        self.db = {}
        self.members = []
        self.count = 0

    def incr(self, a):
        self.count = self.count + 1

        return self.count
    def delete(self, a):
        str_a = str(a)
        if str_a in self.db:
            obj = self.db[str_a]
            del self.db[str_a]
            return obj
        else:
            return None

    def get(self, a):
        str_a = str(a)
        if str_a in self.db:
            return self.db[str_a]
        else:
            return None

    @staticmethod
    def make_storable(a):
        if type(a) is int:
            a_str = str(a)
            a_bytes = a_str.encode('utf-8')
        elif type(a) is bytes:
            a_bytes = a
        elif type(a) is str:
            a_bytes = a.encode('utf-8')
        else:
            raise Exception("CANNOT UNDERSTAND TYPE OF " + str(a))
        return a_bytes

    def sadd(self, a, b):
        print("PRETENDING to add ", Redis.make_storable(b), " TO ", a)
        self.members.append(Redis.make_storable(b))
        return True

    def set(self, a, b):
        self.db[a] = Redis.make_storable(b)
        return True

    def smembers(self, a):
        return self.members

    def srem(self, a, b):
        bencoded = Redis.make_storable(b)
        if bencoded in self.members:
            self.members.remove(bencoded)
        else:
            raise Exception("CANNOT REMOVE (srem) AS NOT IN MEMBERS: " + str(bencoded))
        return True


