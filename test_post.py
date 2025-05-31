import requests

def test_post_chat():
    url = "http://127.0.0.1:8000/api/chat"
    headers = {"Content-Type": "application/json"}
    data = {"message": "Hello, test message from Python script"}

    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.text}")
    except Exception as e:
        print(f"Error sending POST request: {e}")

if __name__ == "__main__":
    test_post_chat()
