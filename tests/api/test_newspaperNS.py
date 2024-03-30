# import the fixtures (this is necessary!)
from ..fixtures import app, client, agency

def test_get_newspaper_should_list_all_papers(client, agency):
    # send request
    response = client.get("/newspaper/")   # <-- note the slash at the end!

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    assert len(parsed["newspapers"]) == len(agency.newspapers)


def test_add_newspaper(client, agency):
    # prepare
    paper_count_before = len(agency.newspapers)

    # act
    response = client.post("/newspaper/",  # <-- note the slash at the end!
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 7,
                               "price": 3.14
                           })
    assert response.status_code == 200
    # verify

    assert len(agency.newspapers) == paper_count_before + 1
    # parse response and check that the correct data is here
    parsed = response.get_json()
    paper_response = parsed["newspaper"]

    # verify that the response contains the newspaper data
    assert paper_response["name"] == "Simpsons Comic"
    assert paper_response["frequency"] == 7
    assert paper_response["price"] == 3.14
def test_get_newspaper_by_id(client, agency):
    # prepare
    paper = agency.newspapers[0]

    # act
    response = client.get(f"/newspaper/{paper.paper_id}")

    # verify
    assert response.status_code == 200
    parsed = response.get_json()
    paper_response = parsed["newspaper"]

    # verify that the response contains the newspaper data
    assert paper_response["paper_id"] == paper.paper_id
    assert paper_response["name"] == paper.name
    assert paper_response["frequency"] == paper.frequency
    assert paper_response["price"] == paper.price
def test_update_newspaper(client, agency):
    # prepare
    paper = agency.newspapers[0]

    # act
    response = client.post(f"/newspaper/{paper.paper_id}",
                           json={
                               "name": "New York Times",
                               "frequency": 6,
                               "price": 10.9
                           })

    # verify
    assert response.status_code == 200
    parsed = response.get_json()
    paper_response = parsed["newspaper"]

    # verify that the response contains the newspaper data
    assert paper_response["paper_id"] == paper.paper_id
    assert paper_response["name"] == "New York Times"
    assert paper_response["frequency"] == 6
    assert paper_response["price"] == 10.9
def test_delete_newspaper(client, agency):
    # prepare
    paper = agency.newspapers[0]
    paper_count_before = len(agency.newspapers)

    # act
    response = client.delete(f"/newspaper/{paper.paper_id}")

    # verify
    assert response.status_code == 200
    assert len(agency.newspapers) == paper_count_before - 1
def test_newspaper_stats(client, agency):
    # prepare
    paper = agency.newspapers[0]
    subscriber = agency.subscribers[0]
    subscriber.subscribe(paper.paper_id)
    # act
    response = client.get(f"/newspaper/{paper.paper_id}/stats")

    # verify
    assert response.status_code == 200
    parsed = response.get_json()
    stats = parsed["newspaper"]

    # verify that the response contains the newspaper data
    assert stats["number_of_subscribers"] == 1
    assert stats["monthly_revenue"] == paper.price * paper.frequency*1
    assert stats["annual_revenue"] == paper.price * paper.frequency*1*12


