from .subscriber import Subscriber
class Issue(object):
    def __init__(self, releasedate: str, released: bool, id: int, editor_id: int,number_of_pages = int):
        self.id = id
        self.releasedate = releasedate
        self.released: bool = released
        self.editor_id = editor_id
        self.number_of_pages = number_of_pages
        self.records = dict()
        self.subscribers = []
    def set_editor(self, editor_id: int):
        if editor_id:
            self.editor_id = editor_id


    def to_dict(self):
        return {
            "issue_id": self.id,  # Update to match the field name in issue_model
            "release_date": self.releasedate,
            "released": self.released,
            "editor_id": self.editor_id,
            "number_of_pages": self.number_of_pages
        }



