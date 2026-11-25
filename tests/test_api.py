
def create_test_user(client):
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "test@example.com"
        }
    )
    return response.json()["id"]


def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "user1@example.com"
        }
    )

    assert response.status_code == 201
    assert response.json()["email"] == "user1@example.com"


def test_get_user(client):
    user_id = create_test_user(client)

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_create_ticket(client):
    user_id = create_test_user(client)

    response = client.post(
        "/tickets",
        json={
            "title": "Test Ticket",
            "description": "Testing ticket creation",
            "status": "open",
            "priority": "high",
            "user_id": user_id
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Test Ticket"


def test_ticket_filtering(client):
    user_id = create_test_user(client)

    client.post(
        "/tickets",
        json={
            "title": "High Priority Ticket",
            "status": "open",
            "priority": "high",
            "user_id": user_id
        }
    )

    response = client.get("/tickets?status=open&priority=high")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["priority"] == "high"


def test_create_and_get_comment(client):
    user_id = create_test_user(client)

    ticket_response = client.post(
        "/tickets",
        json={
            "title": "Comment Test Ticket",
            "user_id": user_id
        }
    )

    ticket_id = ticket_response.json()["id"]

    create_response = client.post(
        f"/tickets/{ticket_id}/comments",
        json={
            "content": "This is a test comment",
            "user_id": user_id
        }
    )

    assert create_response.status_code == 201

    get_response = client.get(f"/tickets/{ticket_id}/comments")

    assert get_response.status_code == 200
    assert len(get_response.json()) == 1


def test_ticket_not_found(client):
    response = client.get("/tickets/999")

    assert response.status_code == 404
