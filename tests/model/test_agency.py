import pytest

from src.model.newspaper import Newspaper
from tests.fixtures import app, client, agency
from src.model.editor import Editor
from src.model.subscriber import Subscriber
def test_add_newspaper(agency):
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    assert len(agency.all_newspapers()) == before + 1


def test_add_newspaper_same_id_should_raise_error(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)

    agency.add_newspaper(new_paper)

    new_paper2 = Newspaper(paper_id=999,
                          name="Superman Comic",
                          frequency=7,
                          price=13.14)

    with pytest.raises(ValueError, match='Newspaper with ID 999 already exists'):  # <-- this allows us to test for exceptions
        # this one should rais ean exception!
        agency.add_newspaper(new_paper2)
    new_paper = Newspaper(paper_id=999,
                          name="",
                          frequency=7,
                          price=3.14)
    with pytest.raises(ValueError, match='Newspaper with ID 999 has missing information'):
        agency.add_newspaper(new_paper)
def test_add_newspaper_missing_info_should_raise_error(agency):
    new_paper = Newspaper(paper_id=9999,
                          name="",
                          frequency=7,
                          price=3.14)
    with pytest.raises(AttributeError, match='Newspaper has missing information'):
        agency.add_newspaper(new_paper)
def test_get_newspaper(agency):
    paper = agency.newspapers[0]
    assert agency.get_newspaper(paper.paper_id) == paper
def test_get_newspaper_not_found(agency):
    with pytest.raises(ValueError, match=f'No newspaper with ID {agency.get_newspaper(9999).paper_id} found'):
        agency.get_newspaper(9999)
def test_get_all_newspapers(agency):
    assert len(agency.all_newspapers()) == len(agency.newspapers)
def test_remove_newspaper(agency):
    paper = agency.newspapers[0]
    before = len(agency.newspapers)
    agency.remove_newspaper(paper.paper_id)
    assert len(agency.all_newspapers()) == before - 1
def test_remove_newspaper_not_found(agency):
    with pytest.raises(AttributeError, match=f'No newspaper with ID 11111 found'):
        agency.remove_newspaper(11111)
def test_update_newspaper(agency):
    paper = agency.newspapers[0]
    new_name = "Updated Name"
    new_frequency = 20
    new_price = 10.5
    updated_paper = agency.update_newspaper(paper.paper_id, new_name, new_frequency, new_price)
    assert updated_paper.name == new_name
    assert updated_paper.frequency == new_frequency
    assert updated_paper.price == new_price
def test_update_newspaper_missing_info_should_raise_error(agency):
    paper = agency.newspapers[0]
    with pytest.raises(AttributeError, match=f'Newspaper has missing information'):
        agency.update_newspaper(paper.paper_id, "", 0, 3.14)
def test_update_newspaper_not_found(agency):
    with pytest.raises(ValueError, match=f'No newspaper with ID {agency.get_newspaper(9999).paper_id} found'):
        agency.update_newspaper(agency.newspapers[agency.get_newspaper(9999)], "New Name", 10, 10.5)
def test_newspaper_stats(agency):
    paper = agency.newspapers[0]
    stats = agency.get_stats_paper(paper.paper_id)
    num = 0
    for subscriber in agency.subscribers:
        if paper.paper_id in subscriber.newspapers:
            num = num + 1
    assert stats["number_of_subscribers"] == num
    assert stats["annual_revenue"] == num*paper.price*paper.frequency*12
    assert stats["monthly_revenue"] == num*paper.price*paper.frequency
def test_newspaper_stats_not_found(agency):
    with pytest.raises(ValueError, match=f'No newspaper with ID {agency.get_newspaper(99999).paper_id} found'):
        agency.get_stats_paper(99999)
def test_add_editor(agency):
    before = len(agency.editors)
    new_editor = Editor(editor_id=111111,
                        editor_name="Lina Boyko",
                        address="Göttweigergasse 5")
    assert agency.add_editor(new_editor)
    assert len(agency.all_editors()) == before + 1
def test_add_editor_missing_info_should_raise_error(agency):
    new_editor = Editor(editor_id=10000,
                        editor_name="",
                        address="Göttweigergasse 5")
    with pytest.raises(AttributeError, match='Editor has missing information'):
        agency.add_editor(new_editor)
def test_add_editor_same_id_should_raise_error(agency):

    new_editor = Editor(editor_id=111111,
                        editor_name="Lina Boyko",
                        address="Göttweigergasse 5")
    assert agency.add_editor(new_editor)

    new_editor = Editor(editor_id=111111,
                        editor_name="Lina Boyko",
                        address="Göttweigergasse 5")
    with pytest.raises(ValueError, match='Editor with ID 111111 already exists'):
        agency.add_editor(new_editor)
def test_get_all_editors(agency):
    assert len(agency.all_editors()) == len(agency.editors)
def test_get_editor(agency):
    editor = agency.editors[0]
    assert agency.get_editor(editor.editor_id) == editor
def test_get_editor_not_found(agency):
    with pytest.raises(ValueError, match=f'No editor with ID {agency.get_editor(9999).editor_id} found'):
        agency.get_editor(9999)
def test_remove_editor(agency):
    editor = agency.editors[0]
    before = len(agency.editors)
    agency.remove_editor(editor.editor_id)
    assert len(agency.all_editors()) == before - 1
def test_remove_editor_not_found(agency):
    editor = Editor(editor_id=9999,
                    editor_name="Lina Boyko",
                    address="Göttweigergasse 5")
    with pytest.raises(ValueError, match=f'No editor with ID {editor.editor_id} found'):
        agency.remove_editor(editor.editor_id)
def test_update_editor(agency):
    editor = agency.editors[0]
    new_name = "Updated Name"
    new_address = "Updated Address"
    updated_editor = agency.update_editor(editor.editor_id, new_name, new_address)
    assert updated_editor.editor_name == new_name
    assert updated_editor.address == new_address
def test_update_editor_not_found(agency):
    with pytest.raises(ValueError, match=f'No editor with ID {agency.get_editor(9999).editor_id} found'):
        agency.update_editor(agency.editors[agency.get_editor(9999)], "New Name", "New Address")
def test_update_editor_missing_info_should_raise_error(agency):
    editor = agency.editors[0]
    with pytest.raises(AttributeError, match=f'Editor has missing information'):
        agency.update_editor(editor.editor_id, "", "")
def test_add_subscriber(agency):
    before = len(agency.subscribers)
    new_subscriber = Subscriber(id=999,
                                sub_name="Lina Boyko",
                                address="Göttweigergasse 5")
    assert agency.add_subscriber(new_subscriber)
    assert len(agency.all_subscribers()) == before + 1
def test_add_subscriber_same_id_should_raise_error(agency):
    before = len(agency.subscribers)
    new_subscriber = Subscriber(id=999,
                                sub_name="Lina Boyko",
                                address="Göttweigergasse 5")
    agency.add_subscriber(new_subscriber)
    new_subscriber = Subscriber(id=999,
                                sub_name="Lina Boyko",
                                address="Göttweigergasse 5")
    with pytest.raises(ValueError, match='Subscriber with ID 999 already exists'):
        agency.add_subscriber(new_subscriber)
def test_add_subscriber_missing_info_should_raise_error(agency):
    new_subscriber = Subscriber(id=10000,
                                sub_name="",
                                address="Göttweigergasse 5")
    with pytest.raises(AttributeError, match='Subscriber has missing information'):
        agency.add_subscriber(new_subscriber)

def test_update_subscriber(agency):
    subscriber = agency.subscribers[0]
    new_name = "Updated Name"
    new_address = "Updated Address"
    updated_subscriber = agency.update_subscriber(subscriber.id, new_name, new_address)
    assert updated_subscriber.sub_name == new_name
    assert updated_subscriber.address == new_address
def test_update_subscriber_not_found(agency):
    with pytest.raises(ValueError, match=f'No subscriber with ID {agency.get_subscriber(9999).id} found'):
        agency.update_subscriber(9999, "New Name", "New Address")
def test_update_subscriber_missing_info_should_raise_error(agency):
    subscriber = agency.subscribers[0]
    with pytest.raises(AttributeError, match='Subscriber has missing information'):
        agency.update_subscriber(subscriber.id, "", "")

def test_get_all_subscribers(agency):
    assert len(agency.all_subscribers()) == len(agency.subscribers)
def test_get_subscriber(agency):
    subscriber = agency.subscribers[0]
    assert agency.get_subscriber(subscriber.id) == subscriber
def test_get_subscriber_not_found(agency):
    with pytest.raises(ValueError, match=f'No subscriber with ID {agency.get_subscriber(9999).id} found'):
        agency.get_subscriber(9999)
def test_remove_subscriber(agency):
    subscriber = agency.subscribers[0]
    before = len(agency.subscribers)
    agency.remove_subscriber(subscriber.id)
    assert len(agency.all_subscribers()) == before - 1
def test_remove_subscriber_not_found(agency):
    with pytest.raises(AttributeError, match=f'No subscriber with ID 22222 found'):
        agency.remove_subscriber(22222)
def test_missing_issues(agency):
    subscriber = agency.subscribers[0]
    missing_issues = []
    missing_issues1 = []

    for newspaper in agency.newspapers:
        for issue in newspaper.issues:
            if subscriber.id not in issue.records and issue.id not in missing_issues:
                missing_issues.append(issue.id)
    print(missing_issues)
    for issue in agency.missing_issues(subscriber.id):
        missing_issues1.append(issue["missing_issues"][0])
    assert len(missing_issues1) == len(missing_issues)
def test_missing_issues_not_found(agency):
    with pytest.raises(AttributeError, match=f'No subscriber with ID 9999 found'):
        agency.missing_issues(9999)
def test_sub_stats(agency):
    subscriber = agency.subscribers[0]
    stats = agency.get_stats(subscriber.id)
    assert stats["number_of_subscriptions"] == len(subscriber.newspapers)
    assert stats["monthly_cost"] == sum(
        [newspaper.price * newspaper.frequency if newspaper.paper_id in subscriber.newspapers else 0 for newspaper in
         agency.newspapers])
    assert stats["annual_cost"] == sum(
        [newspaper.price * newspaper.frequency if newspaper.paper_id in subscriber.newspapers else 0 for newspaper in
         agency.newspapers]) * 12
    assert len(stats["newspapers"]) == len(subscriber.newspapers)
def test_sub_stats_not_found(agency):
    with pytest.raises(AttributeError, match=f'No subscriber with ID 9999 found'):
        agency.get_stats(9999)
def test_subscribe(agency):
    subscriber = agency.subscribers[0]
    paper = agency.newspapers[0]
    before = len(subscriber.newspapers)
    agency.subscribe(subscriber.id, paper.paper_id)
    assert len(subscriber.newspapers) == before + 1
def test_subscribe_not_found(agency):
    with pytest.raises(AttributeError, match=f'No subscriber with ID 9999 found'):
        agency.subscribe(9999, agency.newspapers[0].paper_id)
def test_subscribe_paper_not_found(agency):
    with pytest.raises(AttributeError, match=f'No newspaper with ID 111111 found'):
        agency.subscribe(agency.subscribers[0].id, 111111)
def test_subscribe_already_subscribed(agency):
    subscriber = agency.subscribers[0]
    paper = agency.newspapers[1]
    agency.subscribe(subscriber.id, paper.paper_id)
    with pytest.raises(AttributeError, match=f'Subscriber has already subscribed to paper with ID {paper.paper_id}'):
        agency.subscribe(subscriber.id, paper.paper_id)




