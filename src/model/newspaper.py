from typing import List

from flask import jsonify
from flask_restx import Model

from .issue import Issue


class Newspaper(object):

    def __init__(self, paper_id: int, name: str, frequency: int, price: float):
        self.paper_id: int = paper_id
        self.name: str = name
        self.frequency: int = frequency  # the issue frequency (in days)
        self.price: float = price  # the monthly price
        self.issues: List[Issue] = []
    def all_issues(self) -> List[Issue]:
        return self.issues

    def add_issue(self, issue: Issue):
        if issue.id not in [i.id for i in self.issues]:#
            if issue.number_of_pages > 0:
                self.issues.append(issue)
            else:
                raise ValueError(f"Number of pages must be greater than 0")
        else:
            raise ValueError(f"Issue with ID {issue.id} already exists")
    def remove_issue(self, issue_id: int):
        if issue_id not in [i.id for i in self.issues]:
            raise ValueError(f"No issue with ID {issue_id} found")
        for issue in self.issues:
            if issue.id == issue_id:
                self.issues.remove(issue)

    def to_dict(self):
        return {
            "paper_id": self.paper_id,
            "name": self.name,
            "frequency": self.frequency,
            "price": self.price
        }
    def get_issue(self, issue_id: int) -> Issue:
        for issue in self.issues:
            if issue.id == issue_id:
                return issue
        raise ValueError(f"No issue with ID {issue_id} found")
