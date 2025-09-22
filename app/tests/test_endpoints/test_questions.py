import pytest


@pytest.mark.asyncio
async def test_create_question(async_client):
    test_json = {"text": "Is it a Test Question?"}
    response = await async_client.post("/questions/", json=test_json)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["text"] == test_json["text"]


@pytest.mark.asyncio
async def test_create_question_with_existing_text(question, async_client):
    test_json = {"text": question.text}
    response = await async_client.post("/questions/", json=test_json)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_question(question, answer, async_client):
    response = await async_client.get(f"/questions/{question.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == question.id
    assert data["text"] == question.text
    assert data["created_at"] == question.created_at.isoformat()
    assert isinstance(data["answers"], list)
    assert data["answers"][0]["id"] == answer.id


@pytest.mark.asyncio
async def test_get_questions(question, another_question, async_client):
    response = await async_client.get("/questions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["text"] in [question.text, another_question.text]


@pytest.mark.asyncio
async def test_edit_question(question, async_client):
    edit_json = {"text": "Is it an Edited Question?"}
    response = await async_client.patch(
        f"/questions/{question.id}", json=edit_json
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == question.id
    assert data["text"] == edit_json["text"]


@pytest.mark.asyncio
async def test_delete_question(question, async_client):
    response = await async_client.delete(f"/questions/{question.id}")
    assert response.status_code == 204

    response = await async_client.get(f"/questions/{question.id}")
    assert response.status_code == 404
