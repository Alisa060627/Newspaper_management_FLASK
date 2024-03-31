import pytest

from tests.fixtures import app, client, agency
def test_set_editor(agency):
    issue = agency.newspapers[0].issues[0]
    editor = agency.editors[0]
    issue.set_editor(editor)
    issue_editor = issue.editor_id
    assert issue_editor.editor_id == editor.editor_id

def test_to_dict(agency):
    issue = agency.newspapers[0].issues[0]
    issue_dict = issue.to_dict()
    assert issue_dict["release_date"] == issue.releasedate
    assert issue_dict["released"] == issue.released
    assert issue_dict["editor_id"] == issue.editor_id
    assert issue_dict["number_of_pages"] == issue.number_of_pages
def test_remove_subscriber(agency):
    issue = agency.newspapers[0].issues[0]
    subscriber = agency.subscribers[0]
    issue.remove_subscriber(subscriber)
    subscribers = issue.records.keys()
    assert subscriber not in subscribers

