# bruteforce.py

class BruteForceIndex:
    def __init__(self):
        self.data = []

    def insert(self, key, value):
        self.data.append((key, value))

    def search(self, key):
        for k, v in self.data:
            if k == key:
                return (True,v)
        return (False,None)

    def delete(self, key):
        for i, (k, v) in enumerate(self.data):
            if k == key:
                self.data.pop(i)
                return True
        return False

    def update(self, key, new_value):
        for i, (k, v) in enumerate(self.data):
            if k == key:
                self.data[i] = (key, new_value)
                return True
        return False

    def get_all(self):
        return self.data.copy()
    def range_query ( self , start , end ) :
            return [item for item in self.data if start <= item[0] <= end]
