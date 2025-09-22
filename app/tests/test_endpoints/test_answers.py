import random

import pytest


@pytest.mark.asyncio
async def test_create_answer(async_client, question):
    test_json = {
        "text": "This is a Test Answer.",
        "user_id": str(random.randint(1, 100)),
    }
    response = await async_client.post(
        f"/questions/{question.id}/answers", json=test_json
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["text"] == test_json["text"]
    assert data["question_id"] == question.id
    assert data["user_id"] == test_json["user_id"]


@pytest.mark.asyncio
async def test_create_answer_to_nonexistent_question(async_client):
    test_json = {
        "text": "This is a Test Answer.",
        "user_id": str(random.randint(1, 100)),
    }
    response = await async_client.post(
        f"/questions/{random.randint(1, 100)}/answers", json=test_json
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_answer(async_client, answer):
    response = await async_client.get(f"/answers/{answer.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["text"] == answer.text
    assert data["question_id"] == answer.question_id
    assert data["user_id"] == answer.user_id
    assert data["created_at"] == answer.created_at.isoformat()


@pytest.mark.asyncio
async def test_get_nonexistent_answer(async_client):
    response = await async_client.get(f"/answers/{random.randint(1, 100)}")
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_delete_answer(async_client, answer):
    response = await async_client.delete(f"/answers/{answer.id}")
    assert response.status_code == 204

    get_response = await async_client.get(f"/answers/{answer.id}")
    assert get_response.status_code == 409
