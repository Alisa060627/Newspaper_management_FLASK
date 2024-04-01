class Subscriber(object):
    def __init__(self, id: int, sub_name: str, address: str):
        self.id = id
        self.newspapers = []
        self.sub_name = sub_name
        self.address = address
    def to_dict(self):
        return {
            "id": self.id,
            "sub_name": self.sub_name,
            "address": self.address
        }







