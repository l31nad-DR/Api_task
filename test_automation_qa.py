import requests

ENDPOINT = "https://demoqa.com"  # This url is for the API requests
head = {"Content-Type": "application/json"}  # Header for the requests
# Placeholder variables for user ID and token
user_id = ""
token = ""

# Username and password for creating the new user
payload = {
        "userName": "Test_User_30",
        "password": "P@rola123"
}


# Function to create a user using the provided body
def create_user(body):
    return requests.post(ENDPOINT + "/Account/v1/User", json=body)


# Task 1
# Trying to create a user with invalid password
def test_1():
    # That is the body, that is put in the request for the creation of the user.
    # The body has a valid userName, but invalid password
    body = {
        "userName": "test_user_1",
        "password": "passwd"
    }
    response = create_user(body)
    assert response.status_code == 400


# Trying to create a user with already existing userName
def test_2():
    body = {
        "userName": "test_user_1",
        "password": "P@sswd123"
    }
    response = create_user(body)
    assert response.status_code == 406


# Task 2
# Function to create a user and store user ID
def test_create_user():
    create_user_response = create_user(payload)
    assert create_user_response.status_code == 201
    user_data = create_user_response.json()
    global user_id
    user_id = user_data['userID']


# Function to get an authentication token and set authorization header
def test_get_token():
    get_token_response = requests.post(ENDPOINT + "/Account/v1/GenerateToken", json=payload)
    assert get_token_response.status_code == 200
    token_data = get_token_response.json()
    global token
    token = token_data["token"]
    head["Authorization"] = f"Bearer {token}"


# Function to check if the user is authorized
def test_authorized():
    check_authorized_response = requests.post(ENDPOINT + "/Account/v1/Authorized", json=payload)
    assert check_authorized_response.status_code == 200


# Function to get user details using the stored user ID and token
def test_get_user():
    get_user_response = requests.get(ENDPOINT + f"/Account/v1/User/{user_id}", headers=head)
    assert get_user_response.status_code == 200


# Task 3
# Test function to create a book list for a user
def test_add_books_list():
    # Create a book list with the user ID and the ISBN of the fourth book
    book_list = {
        "userId": f"{user_id}",
        "collectionOfIsbns": [{"isbn": f"{get_fourth_book()}"}]
    }
    # Send a request to add the book list and assert the response status code
    list_of_books_response = requests.post(ENDPOINT + "/BookStore/v1/Books", json=book_list, headers=head)
    assert list_of_books_response.status_code == 201


# Function to get the ISBN of the fourth book from the bookstore
def get_fourth_book():
    get_book_response = requests.get(ENDPOINT + "/BookStore/v1/Books")
    assert get_book_response.status_code == 200
    book_data = get_book_response.json()
    books_list = book_data["books"]
    return books_list[3]["isbn"]


# Task 4
# Test function to add a book with a wrong ISBN
def test_wrong_book():
    # Create a book list with the user ID and a wrong ISBN
    book_list = {
        "userId": f"{user_id}",
        "collectionOfIsbns": [{"isbn": "7895421"}]
    }
    # Send a request to add the book list with a wrong ISBN and assert the response status code
    wrong_book_response = requests.post(ENDPOINT + "/BookStore/v1/Books", json=book_list, headers=head)
    assert wrong_book_response.status_code == 400


# Task 5
# Test function to replace the first book in the user's collection
def test_replace_first_book():
    # Get the user's data to retrieve the ISBN of the first book
    get_user_response = requests.get(ENDPOINT + f"/Account/v1/User/{user_id}", headers=head)
    user_data = get_user_response.json()
    user_first_book = user_data["books"][0]
    # Prepare the body to delete the first book
    body = {
        "isbn": f"{user_first_book['isbn']}",
        "userId": f"{user_id}"
    }
    # Send a request to delete the first book and assert the response status code
    delete_user_book_response = requests.delete(ENDPOINT + "/BookStore/v1/Book", json=body, headers=head)
    assert delete_user_book_response.status_code == 204
    # Add a book to the user's collection
    book_list = {
        "userId": f"{user_id}",
        "collectionOfIsbns": [{"isbn": f"{get_second_book()}"}]
    }
    # Send a request to add the new book list and assert the response status code
    list_of_books_response = requests.post(ENDPOINT + "/BookStore/v1/Books", json=book_list, headers=head)
    assert list_of_books_response.status_code == 201


# Function to get the ISBN of the second book from the bookstore
def get_second_book():
    get_book_response = requests.get(ENDPOINT + "/BookStore/v1/Books")
    assert get_book_response.status_code == 200
    book_data = get_book_response.json()
    books_list = book_data["books"]
    return books_list[1]["isbn"]


# Task 6
# Test function to retrieve and verify book details
def test_book():
    # Send a request to get book details using ISBN and assert the response status code
    get_book_response = requests.get(ENDPOINT + "/BookStore/v1/Book?ISBN=9781491904244")
    assert get_book_response.status_code == 200
    # Assert that the number of pages matches the expected value
    book_data = get_book_response.json()
    pages = book_data["pages"]
    assert pages == 278


# Task 7
# Test function to delete the first book in the user's collection
def test_delete_book():
    # Send a GET request to retrieve user data
    get_user_response = requests.get(ENDPOINT + f"/Account/v1/User/{user_id}", headers=head)
    user_data = get_user_response.json()
    # Extract the first book from the user's collection
    user_first_book = user_data["books"][0]

    body = {
        "isbn": f"{user_first_book['isbn']}",
        "userId": f"{user_id}"
    }
    # Send a DELETE request to remove the user's book and assert the response status code
    delete_user_book_response = requests.delete(ENDPOINT + "/BookStore/v1/Book", json=body, headers=head)
    assert delete_user_book_response.status_code == 204


# Task 8
# Test function to delete a book with wrong ISBN from the user's collection
def test_delete_wrong_book():
    # Prepare data for the DELETE request with a wrong ISBN
    body = {
        "isbn": "754213154",
        "userId": f"{user_id}"
    }
    # Send a DELETE request to attempt to remove a book with a wrong ISBN and assert the response status code
    delete_user_book_response = requests.delete(ENDPOINT + "/BookStore/v1/Book", json=body, headers=head)
    assert delete_user_book_response.status_code == 400
