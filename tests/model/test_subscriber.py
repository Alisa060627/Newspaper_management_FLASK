import pytest
from tests.fixtures import app, client, agency
from src.model.subscriber import Subscriber
def test_to_dict(agency):
    subscriber = agency.subscribers[0]
    subscriber_dict = subscriber.to_dict()
    assert subscriber_dict["id"] == subscriber.id
    assert subscriber_dict["sub_name"] == subscriber.sub_name
    assert subscriber_dict["address"] == subscriber.address

