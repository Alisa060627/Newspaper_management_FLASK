import pytest
from tests.fixtures import app, client, agency
from src.model.issue import Issue
def test_add_issue(agency):
    newspaper = agency.newspapers[0]
    before = len(newspaper.issues)
    new_issue = Issue(id=999,
                        releasedate="2021-01-01T00:00:00Z",
                        released=False,
                        editor_id=agency.editors[0].editor_id,
                        number_of_pages=10)
    newspaper.add_issue(new_issue)
    assert len(newspaper.issues) == before + 1
def test_add_issue_same_id_should_raise_error(agency):
    newspaper = agency.newspapers[0]
    before = len(newspaper.issues)
    new_issue = Issue(id=999,
                        releasedate="2021-01-01T00:00:00Z",
                        released=False,
                        editor_id=agency.editors[0].editor_id,
                        number_of_pages=10)
    newspaper.add_issue(new_issue)
    assert len(newspaper.issues) == before + 1
def test_get_all_issues(agency):
    newspaper = agency.newspapers[0]
    assert len(newspaper.all_issues()) == len(newspaper.issues)
def test_get_issue(agency):
    newspaper = agency.newspapers[0]
    issue = newspaper.issues[0]
    assert newspaper.get_issue(issue.id) == issue
def test_get_issue_not_found(agency):
    newspaper = agency.newspapers[0]
    assert newspaper.get_issue(99909)
def test_to_dict(agency):
    newspaper = agency.newspapers[0]
    newspaper_dict = newspaper.to_dict()
    assert newspaper_dict["paper_id"] == newspaper.paper_id
    assert newspaper_dict["name"] == newspaper.name
    assert newspaper_dict["price"] == newspaper.price
    assert newspaper_dict["frequency"] == newspaper.frequency