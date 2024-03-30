import pytest
from tests.fixtures import app, client, agency
from src.model.subscriber import Subscriber
def test_to_dict(agency):
    subscriber = agency.subscribers[0]
    subscriber_dict = subscriber.to_dict()
    assert subscriber_dict["sub_id"] == subscriber.id
    assert subscriber_dict["sub_name"] == subscriber.sub_name
    assert subscriber_dict["address"] == subscriber.address
def test_add_subscription(agency):
    subscriber = agency.subscribers[0]
    before = len(subscriber.newspapers)
    newspaper = agency.newspapers[0]
    subscriber.subscribe(newspaper)
    assert len(subscriber.newspapers) == before + 1
def test_add_subscription_already_exists(agency):
    subscriber = agency.subscribers[0]
    before = len(subscriber.newspapers)
    newspaper = agency.newspapers[0]
    subscriber.subscribe(newspaper)
    assert len(subscriber.newspapers) == before + 1