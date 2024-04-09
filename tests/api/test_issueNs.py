from ..fixtures import app, client, agency

def test_add_issue(client, agency):
    # Get a valid paper_id from the agency
    paper = agency.newspapers[0]
    issue_count_before = len(paper.issues)
    response = client.post(f"/newspaper/{paper.paper_id}/issue",
                            json={
                                "release_date": "2020-01-01T00:00:00",
                                "released": False,
                                "editor_id": 1,
                                "number_of_pages": 10
                            })
    assert response.status_code == 200

    # verify
    assert len(paper.issues) == issue_count_before + 1

    # parse response and check that the correct data is here
    parsed = response.get_json()
    issue_response = parsed["issue"]

    # verify that the response contains the newspaper data
    assert issue_response["release_date"] == "2020-01-01T00:00:00"
    assert issue_response["released"] == False
    assert issue_response["editor_id"] == 1
    assert issue_response["number_of_pages"] == 10
def test_get_all_issues(client, agency):
    paper = agency.newspapers[0]
    response = client.get(f"/newspaper/{paper.paper_id}/issue")
    assert response.status_code == 200
    parsed = response.get_json()
    issues_response = parsed["issues"]
    assert len(issues_response) == len(paper.issues)


def test_get_issue(client, agency):
    paper = agency.newspapers[0]
    issue = paper.issues[0]
    response = client.get(f"/newspaper/{paper.paper_id}/issue/{issue.id}")
    assert response.status_code == 200
    parsed = response.get_json()
    issue_response = parsed["issue"]
    assert issue_response["release_date"] == issue.releasedate
    assert issue_response["released"] == issue.released
    assert issue_response["editor_id"] == issue.editor_id
    assert issue_response["number_of_pages"] == issue.number_of_pages
def test_delete_issue(client, agency):
    paper = agency.newspapers[0]
    issue = paper.issues[0]
    response = client.delete(f"/newspaper/{paper.paper_id}/issue/{issue.id}")
    assert response.status_code == 200
    assert issue not in paper.issues
def test_release_issue(client, agency):
    paper = agency.newspapers[0]
    issue = paper.issues[0]
    response = client.post(f"/newspaper/{paper.paper_id}/issue/{issue.id}/release")
    assert response.status_code == 200
    parsed = response.get_json()
    issue_response = parsed["issue"]
    assert issue_response["released"] == True

def test_issue_set_editor(client, agency):
    paper = agency.newspapers[0]
    issue = paper.issues[0]
    response = client.post(f"/newspaper/{paper.paper_id}/issue/{issue.id}/editor",
                           json={"editor_id": agency.editors[0].editor_id})
    assert response.status_code == 200
    parsed = response.get_json()
    issue_response = parsed["issue"]
    assert issue_response["editor_id"] == agency.editors[0].editor_id
def test_issue_deliver(client, agency):

    paper = agency.newspapers[0]
    subscriber = agency.subscribers[0]
    issue = paper.issues[0]
    agency.subscribe(subscriber.id,paper.paper_id)
    response = client.post(f"/newspaper/{paper.paper_id}/issue/{issue.id}/deliver", json={"subscriber_id": subscriber.id})
    assert response.status_code == 200
    assert subscriber.id in issue.records
