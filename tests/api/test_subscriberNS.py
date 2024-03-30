from ..fixtures import app, client, agency
def test_add_subscriber(client, agency):
    # Get a valid paper_id from the agency
    paper = agency.newspapers[0]
    response = client.post(f"/subscriber/",
                            json={
                                "sub_name": "Nick Davidson",
                                "address": "Prinz-Eugen-Straße 51"})
    assert response.status_code == 200
    parsed = response.get_json()
    subscriber_response = parsed["subscriber"]
    assert subscriber_response["sub_name"] == "Nick Davidson"
    assert subscriber_response["address"] == "Prinz-Eugen-Straße 51"
def test_get_all_subscribers(client, agency):
    paper = agency.newspapers[0]
    response = client.get("/subscriber/")
    assert response.status_code == 200
    parsed = response.get_json()
    subscribers_response = parsed["subscriber"]
    assert len(subscribers_response) == len(agency.subscribers)
def test_get_subscriber(client, agency):
    paper = agency.newspapers[0]
    subscriber = agency.subscribers[0]
    response = client.get(f"/subscriber/{subscriber.id}")
    assert response.status_code == 200
    parsed = response.get_json()
    subscriber_response = parsed["subscriber"]
    assert subscriber_response["sub_name"] == subscriber.sub_name
    assert subscriber_response["address"] == subscriber.address
def test_update_subscriber(client, agency):
    paper = agency.newspapers[0]
    subscriber = agency.subscribers[0]
    response = client.post(f"/subscriber/{subscriber.id}",
                            json={
                                "sub_name": "Mark Bauer",
                                "address": "Hasenleitengasse 1"})
    assert response.status_code == 200
    parsed = response.get_json()
    subscriber_response = parsed["subscriber"]
    assert subscriber_response["sub_name"] == "Mark Bauer"
    assert subscriber_response["address"] == "Hasenleitengasse 1"
def test_delete_subscriber(client, agency):
    paper = agency.newspapers[0]
    subscriber = agency.subscribers[0]
    response = client.delete(f"/subscriber/{subscriber.id}")
    assert response.status_code == 200
    assert subscriber not in agency.subscribers
def test_subscribe(client, agency):
    paper = agency.newspapers[0]
    subscriber = agency.subscribers[0]
    response = client.post(f"/subscriber/{subscriber.id}/subscribe",
                            json={"newspaper_id": paper.paper_id})
    assert response.status_code == 200
    assert paper.paper_id in subscriber.newspapers
def test_missing_issues(client, agency):
    paper = agency.newspapers[0]
    subscriber = agency.subscribers[0]
    response = client.get(f"/subscriber/{subscriber.id}/missingissues")
    assert response.status_code == 200
    parsed = response.get_json()
    assert len(parsed["issues"]) == len(agency.missing_issues(subscriber))
def test_subscriber_stats(client, agency):
    paper = agency.newspapers[0]
    subscriber = agency.subscribers[1]
    subscriber.subscribe(paper.paper_id)
    response = client.get(f"/subscriber/{subscriber.id}/stats")
    assert response.status_code == 200
    parsed = response.get_json()
    assert parsed["stats"]["number_of_subscriptions"] == len(subscriber.newspapers)
    assert parsed["stats"]["monthly_cost"] == sum([newspaper.price*newspaper.frequency if newspaper.paper_id in subscriber.newspapers else 0 for newspaper in agency.newspapers])
    assert parsed["stats"]["annual_cost"] == sum([newspaper.price*newspaper.frequency if newspaper.paper_id in subscriber.newspapers else 0 for newspaper in agency.newspapers])*12
    assert len(parsed["stats"]["newspapers"])== len(subscriber.newspapers)
