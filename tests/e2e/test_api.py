import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')
))

from playwright.sync_api import APIRequestContext, Playwright
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─── FIXTURE: API context ───
@pytest.fixture
def api(playwright: Playwright):
    request_context = playwright.request.new_context(
        base_url=BASE_URL
    )
    yield request_context
    request_context.dispose()


# ─── TEST 1: GET all users ───
def test_get_all_users(api: APIRequestContext):

    response = api.get("/users")

    assert response.status == 200
    body = response.json()

    assert len(body) == 10
    print(f"✓ Status: {response.status}")
    print(f"✓ Total users found: {len(body)}")


# ─── TEST 2: GET single user ───
def test_get_single_user(api: APIRequestContext):

    response = api.get("/users/1")

    assert response.status == 200
    user = response.json()

    assert user["id"] == 1
    assert "name" in user
    assert "email" in user
    print(f"✓ User ID: {user['id']}")
    print(f"✓ Name: {user['name']}")
    print(f"✓ Email: {user['email']}")


# ─── TEST 3: GET user not found ───
def test_get_user_not_found(api: APIRequestContext):

    response = api.get("/users/999")

    assert response.status == 404
    print(f"✓ Correctly returned 404 for missing user")


# ─── TEST 4: GET all posts ───
def test_get_all_posts(api: APIRequestContext):

    response = api.get("/posts")

    assert response.status == 200
    body = response.json()

    assert len(body) == 100
    print(f"✓ Total posts: {len(body)}")


# ─── TEST 5: GET single post ───
def test_get_single_post(api: APIRequestContext):

    response = api.get("/posts/1")

    assert response.status == 200
    post = response.json()

    assert post["id"] == 1
    assert "title" in post
    assert "body" in post
    print(f"✓ Post ID: {post['id']}")
    print(f"✓ Title: {post['title']}")


# ─── TEST 6: POST create new post ───
def test_create_post(api: APIRequestContext):

    new_post = {
        "title": "Playwright API Testing",
        "body": "Learning API testing with Playwright Python",
        "userId": 1
    }

    response = api.post("/posts", data=new_post)

    assert response.status == 201
    body = response.json()

    assert body["title"] == "Playwright API Testing"
    assert "id" in body
    print(f"✓ Post created!")
    print(f"✓ New post ID: {body['id']}")
    print(f"✓ Title: {body['title']}")


# ─── TEST 7: PUT update post ───
def test_update_post(api: APIRequestContext):

    updated_post = {
        "id": 1,
        "title": "Updated Playwright Testing",
        "body": "Updated content",
        "userId": 1
    }

    response = api.put("/posts/1", data=updated_post)

    assert response.status == 200
    body = response.json()

    assert body["title"] == "Updated Playwright Testing"
    print(f"✓ Post updated!")
    print(f"✓ New title: {body['title']}")


# ─── TEST 8: DELETE post ───
def test_delete_post(api: APIRequestContext):

    response = api.delete("/posts/1")

    assert response.status == 200
    print(f"✓ Post deleted! Status: {response.status}")


# ─── TEST 9: GET comments for a post ───
def test_get_comments(api: APIRequestContext):

    response = api.get("/posts/1/comments")

    assert response.status == 200
    comments = response.json()

    assert len(comments) == 5
    print(f"✓ Comments found: {len(comments)}")

    # Check each comment has required fields
    for comment in comments:
        assert "email" in comment
        assert "body" in comment
    print("✓ All comments have correct structure")


# ─── TEST 10: API + UI Combined ───
def test_api_then_ui(api: APIRequestContext, page):

    # STEP 1: Get user data via API
    response = api.get("/users/1")
    assert response.status == 200
    user = response.json()
    print(f"✓ API: Got user — {user['name']}")

    # STEP 2: Get their posts via API
    posts_response = api.get(f"/posts?userId={user['id']}")
    posts = posts_response.json()
    print(f"✓ API: User has {len(posts)} posts")

    # STEP 3: Open UI and verify
    page.goto("https://jsonplaceholder.typicode.com")
    page.wait_for_load_state("networkidle")
    assert "JSONPlaceholder" in page.title()
    print(f"✓ UI: Website loaded — {page.title()}")

    page.screenshot(path="screenshots/api_ui_combined.png")
    print("✓ Combined API + UI test complete!")