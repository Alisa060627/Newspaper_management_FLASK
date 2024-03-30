import pytest

from tests.fixtures import app, client, agency
def test_to_dict(agency):
    editor = agency.editors[0]
    editor_dict = editor.to_dict()
    assert editor_dict["editor_id"] == editor.editor_id
    assert editor_dict["editor_name"] == editor.editor_name
    assert editor_dict["address"] == editor.address
def test_add_newspaper(agency):
    editor = agency.editors[0]
    before = len(editor.newspapers)
    editor.add_newspaper(agency.newspapers[0])
    assert len(editor.newspapers) == before + 1
def test_all_issues(agency):
    editor = agency.editors[0]
    issues = []
    for newspaper in editor.newspapers:
        for issue in newspaper.issues:
            if issue.editor_id == editor.editor_id:
                issues.append(issue)
    assert len(editor.all_issues()) == len(issues)

