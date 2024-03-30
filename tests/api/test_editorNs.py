from ..fixtures import app, client, agency
def test_get_all_editors(client, agency):
    response = client.get("/editor/")
    assert response.status_code == 200
    parsed = response.get_json()
    editors_response = parsed["editors"]
    assert len(editors_response) == len(agency.editors)
def test_get_editor(client, agency):
    editor = agency.editors[0]
    response = client.get(f"/editor/{editor.editor_id}")
    assert response.status_code == 200
    parsed = response.get_json()
    editor_response = parsed["editor"]
    assert editor_response["editor_id"] == editor.editor_id
    assert editor_response["editor_name"] == editor.editor_name
    assert editor_response["address"] == editor.address
def test_add_editor(client, agency):
    aditor_count_before = len(agency.editors)
    response = client.post("/editor/", json={
        "editor_name": "Micky Bauer",
        "address": "Schönbrunner Straße 45"
    })
    assert response.status_code == 200
    parsed = response.get_json()
    editor_response = parsed["editor"]
    assert editor_response["editor_name"] == "Micky Bauer"
    assert editor_response["address"] == "Schönbrunner Straße 45"
    assert len(agency.editors) == aditor_count_before + 1
def test_update_editor(client, agency):
    editor = agency.editors[0]
    response = client.post(f"/editor/{editor.editor_id}", json={
        "editor_name": "Alisa Beztsinna",
        "address": "Karl-Eybl-Gasse 5"
    })
    assert response.status_code == 200
    parsed = response.get_json()
    editor_response = parsed["editor"]
    assert editor_response["editor_name"] == "Alisa Beztsinna"
    assert editor_response["address"] == "Karl-Eybl-Gasse 5"
    assert editor_response["editor_id"] == editor.editor_id
def test_delete_editor(client, agency):
    editor = agency.editors[0]
    editor_count_before = len(agency.editors)
    response = client.delete(f"/editor/{editor.editor_id}")
    assert response.status_code == 200
    assert editor not in agency.editors
    assert len(agency.editors) == editor_count_before - 1
def test_get_all_issues_of_editor(client, agency):
    editor = agency.editors[0]
    response = client.get(f"/editor/{editor.editor_id}/issues")
    assert response.status_code == 200
    parsed = response.get_json()
    issues_response = parsed["issues"]
    issues = []
    for newspaper in editor.newspapers:
        for issue in newspaper.issues:
            if issue.editor_id == editor.editor_id:
                issues.append(issue)
    assert len(issues_response) == len(issues)