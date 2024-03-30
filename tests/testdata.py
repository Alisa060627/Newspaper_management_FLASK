from src.model.agency import Agency
from src.model.newspaper import Newspaper
from src.model.subscriber import Subscriber
from src.model.issue import Issue
from src.model.editor import Editor
def create_newspapers(agency: Agency):
    paper1 = Newspaper(paper_id=100, name="The New York Times", frequency=7, price=13.14)
    paper2 = Newspaper(paper_id=101, name="Heute", frequency=1, price=1.12)
    paper3 = Newspaper(paper_id=115, name="Wall Street Journal", frequency=1, price=3.00)
    paper4 = Newspaper(paper_id=125, name="National Geographic", frequency=30, price=34.00)
    agency.newspapers.extend([paper1, paper2, paper3, paper4])


def populate(agency: Agency):
    create_newspapers(agency)
    create_subscribers(agency)
    create_editors(agency)
    create_issues(agency)
def create_issues(agency: Agency):
    issue1 = Issue(id=300, releasedate="2020-01-01T00:00:00", released=False, editor_id=1, number_of_pages=10)
    issue2 = Issue(id=301, releasedate="2020-01-01T00:00:00", released=False, editor_id=1, number_of_pages=10)
    issue3 = Issue(id=302, releasedate="2020-01-01T00:00:00", released=False, editor_id=1, number_of_pages=10)
    issue4 = Issue(id=303, releasedate="2020-01-01T00:00:00", released=False, editor_id=1, number_of_pages=10)
    agency.newspapers[0].issues.extend([issue1, issue2, issue3, issue4])
    agency.newspapers[1].issues.extend([issue1, issue2, issue3, issue4])
    agency.newspapers[2].issues.extend([issue1, issue2, issue3, issue4])
    agency.newspapers[3].issues.extend([issue1, issue2, issue3, issue4])
def create_subscribers(agency: Agency):
    subscriber1 = Subscriber(id=200, sub_name="Hans", address="Hauptstrasse 1")
    subscriber2 = Subscriber(id=2001, sub_name="Franz", address="Hauptstrasse 2")
    subscriber3 = Subscriber(id=2002, sub_name="Anna", address="Hauptstrasse 3")
    subscriber4 = Subscriber(id=2003, sub_name="Peter", address="Hauptstrasse 4")
    agency.subscribers.extend([subscriber1, subscriber2, subscriber3, subscriber4])

def create_editors(agency: Agency):
    editor1 = Editor(editor_id=300, editor_name="Hans", address="Hauptstrasse 1")
    editor2 = Editor(editor_id=301, editor_name="Franz", address="Hauptstrasse 2")
    editor3 = Editor(editor_id=302, editor_name="Anna", address="Hauptstrasse 3")
    editor4 = Editor(editor_id=303, editor_name="Peter", address="Hauptstrasse 4")
    agency.editors.extend([editor1, editor2, editor3, editor4])