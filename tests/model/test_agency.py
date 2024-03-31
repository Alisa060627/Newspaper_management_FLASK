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
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)

    # first adding of newspaper should be okay
    agency.add_newspaper(new_paper)

    new_paper2 = Newspaper(paper_id=999,
                          name="Superman Comic",
                          frequency=7,
                          price=13.14)

    with pytest.raises(ValueError, match='A newspaper with ID 999 already exists'):  # <-- this allows us to test for exceptions
        # this one should rais ean exception!
        agency.add_newspaper(new_paper2)
def test_get_newspaper(agency):
    paper = agency.newspapers[0]
    assert agency.get_newspaper(paper.paper_id) == paper
def test_get_newspaper_not_found(agency):
    assert agency.get_newspaper(9999)
def test_get_all_newspapers(agency):
    assert len(agency.all_newspapers()) == len(agency.newspapers)
def test_remove_newspaper(agency):
    paper = agency.newspapers[0]
    before = len(agency.newspapers)
    agency.remove_newspaper(paper)
    assert len(agency.all_newspapers()) == before - 1
def test_remove_newspaper_not_found(agency):
    paper = Newspaper(paper_id=1999,
                      name="Simpsons Comic",
                      frequency=7,
                      price=3.14)
    before = len(agency.newspapers)
    assert agency.remove_newspaper(paper)
    assert len(agency.all_newspapers()) == before
def test_update_newspaper(agency):
    paper = agency.newspapers[0]
    new_name = "Updated Name"
    new_frequency = 20
    new_price = 10.5
    updated_paper = agency.update_newspaper(paper, new_name, new_frequency, new_price)
    assert updated_paper.name == new_name
    assert updated_paper.frequency == new_frequency
    assert updated_paper.price == new_price
def test_update_newspaper_not_found(agency):
    with pytest.raises(ValueError, match=f'No newspaper with ID {agency.get_newspaper(9999).paper_id} found'):
        agency.update_newspaper(agency.newspapers[agency.get_newspaper(9999)], "New Name", 10, 10.5)
def test_add_editor(agency):
    before = len(agency.editors)
    new_editor = Editor(editor_id=111111,
                        editor_name="Lina Boyko",
                        address="Göttweigergasse 5")
    assert agency.add_editor(new_editor)
    assert len(agency.all_editors()) == before + 1
def test_add_editor_same_id_should_raise_error(agency):
    before = len(agency.editors)
    new_editor = Editor(editor_id=111111,
                        editor_name="Lina Boyko",
                        address="Göttweigergasse 5")
    assert agency.add_editor(new_editor)
    assert len(agency.all_editors()) == before + 1
def test_get_all_editors(agency):
    assert len(agency.all_editors()) == len(agency.editors)
def test_get_editor(agency):
    editor = agency.editors[0]
    assert agency.get_editor(editor.editor_id) == editor
def test_get_editor_not_found(agency):
    assert agency.get_editor(9999)
def test_remove_editor(agency):
    editor = agency.editors[0]
    before = len(agency.editors)
    agency.remove_editor(editor)
    assert len(agency.all_editors()) == before - 1
def test_remove_editor_not_found(agency):
    editor = Editor(editor_id=9999,
                    editor_name="Lina Boyko",
                    address="Göttweigergasse 5")
    before = len(agency.editors)
    assert agency.remove_editor(editor)
    assert len(agency.all_editors()) == before
def test_add_subscriber(agency):
    before = len(agency.subscribers)
    new_subscriber = Subscriber(id=999,
                                sub_name="Lina Boyko",
                                address="Göttweigergasse 5")
    assert agency.add_subscriber(new_subscriber)
    assert len(agency.all_subscribers()) == before + 1
def test_update_subscriber(agency):
    subscriber = agency.subscribers[0]
    new_name = "Updated Name"
    new_address = "Updated Address"
    updated_subscriber = agency.update_subscriber(subscriber, new_name, new_address)
    assert updated_subscriber.sub_name == new_name
    assert updated_subscriber.address == new_address
def test_update_subscriber_not_found(agency):
    with pytest.raises(ValueError, match=f'No subscriber with ID {agency.get_subscriber(9999).id} found'):
        agency.update_subscriber(agency.subscribers[agency.get_subscriber(9999)], "New Name", "New Address")

def test_add_subscriber_same_id_should_raise_error(agency):
    before = len(agency.subscribers)
    new_subscriber = Subscriber(id=999,
                                sub_name="Lina Boyko",
                                address="Göttweigergasse 5")
    assert agency.add_subscriber(new_subscriber)
    assert len(agency.all_subscribers()) == before + 1
def test_get_all_subscribers(agency):
    assert len(agency.all_subscribers()) == len(agency.subscribers)
def test_get_subscriber(agency):
    subscriber = agency.subscribers[0]
    assert agency.get_subscriber(subscriber.id) == subscriber
def test_get_subscriber_not_found(agency):
    assert agency.get_subscriber(9999)
def test_remove_subscriber(agency):
    subscriber = agency.subscribers[0]
    before = len(agency.subscribers)
    agency.remove_subscriber(subscriber)
    assert len(agency.all_subscribers()) == before - 1
def test_remove_subscriber_not_found(agency):
    subscriber = Subscriber(id=22222,
                            sub_name="Maria Ivanova",
                            address="Göttweigergasse 5")
    before = len(agency.subscribers)
    assert agency.remove_subscriber(subscriber)
    assert len(agency.all_subscribers()) == before-1







