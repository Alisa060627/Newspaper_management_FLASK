import pytest

from tests.fixtures import app, client, agency
from src.model.editor import Editor
from src.model.newspaper import Newspaper
def test_to_dict(agency):
    editor = Editor("Micky Bauer", 1, "Schönbrunner Straße 45", [Newspaper(400, "New york", 6, 7)])
    editor_dict = editor.to_dict()
    assert editor_dict["editor_id"] == editor.editor_id
    assert editor_dict["editor_name"] == editor.editor_name
    assert editor_dict["address"] == editor.address
    assert editor_dict["newspapers"] == [newspaper.paper_id for newspaper in editor.newspapers]

def test_add_newspaper(agency):
    editor = Editor("Micky Bauer", 1, "Schönbrunner Straße 45", [Newspaper(400, "New york",6,7)])
    editor.add_newspaper(Newspaper(401, "New york",6,7))
    assert len(editor.newspapers) == 2
def test_all_issues(agency):
    editor = Editor("Micky Bauer", 1, "Schönbrunner Straße 45", [Newspaper(400, "New york", 6, 7)])
    issues = []
    for newspaper in editor.newspapers:
        for issue in newspaper.issues:
            if issue.editor_id == editor.editor_id:
                issues.append(issue)
    assert editor.all_issues() == issues

