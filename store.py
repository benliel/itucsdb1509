class Store:
    def __init__(self):
        self.data={}
        self.last_key=0

    def add(self, data):
        self.last_key += 1
        self.data[self.last_key] = data

    def delete(self, key):
        del self.data[key]

    def get(self, key):
        return self.data[key]

    def get(self):
        return sorted(self.data.items())