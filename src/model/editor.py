from src.model.newspaper import Newspaper
class Editor(object):
    def __init__(self, editor_name: str, editor_id: int, address: str):
        self.editor_name = editor_name
        self.editor_id = editor_id
        self.address = address
        self.newspapers = []
    def to_dict(self):
        return {
            "editor_id": self.editor_id,
            "editor_name": self.editor_name,
            "address": self.address
        }
    def add_newspaper(self, newspaper: Newspaper):
        self.newspapers.append(newspaper)
    def all_issues(self):
        issues = []
        for newspaper in self.newspapers:
            issues += newspaper.all_issues()
        return issues