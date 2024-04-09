from src.model.newspaper import Newspaper
class Editor(object):
    def __init__(self, editor_name: str, editor_id: int, address: str, newspapers = []):
        self.editor_name = editor_name
        self.editor_id = editor_id
        self.address = address
        self.newspapers = newspapers
    def to_dict(self):
        return {
            "editor_id": self.editor_id,
            "editor_name": self.editor_name,
            "address": self.address,
            "newspapers": [newspaper.paper_id for newspaper in self.newspapers] if self.newspapers else []
        }
    def add_newspaper(self, newspaper: Newspaper):
        self.newspapers.append(newspaper)
    def all_issues(self):
        issues = []
        for newspaper in self.newspapers:
            for issue in newspaper.issues:
                if issue.editor_id == self.editor_id and issue not in issues:
                    issues.append(issue)
        return issues

