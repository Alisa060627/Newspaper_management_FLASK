
class Issue(object):
    def __init__(self, releasedate: str, released: bool, id: int, editor_id: int,number_of_pages = int):
        self.id = id
        self.releasedate = releasedate
        self.released: bool = released
        self.editor_id = editor_id
        self.records = []
        self.number_of_pages = number_of_pages
    def set_editor(self, editor_id: int):
        self.editor_id = editor_id

    def to_dict(self):
        return {
            "issue_id": self.id,  # Update to match the field name in issue_model
            "release_date": self.releasedate,
            "released": self.released,
            "editor_id": self.editor_id,
            "number_of_pages": self.number_of_pages
        }
    def deliver(self, subscriber_id: int):
        self.records.append(f"Subscriber with id{subscriber_id}received issue with id {self.id}")
        return f"Subscriber with id {subscriber_id} received issue with id {self.id}"