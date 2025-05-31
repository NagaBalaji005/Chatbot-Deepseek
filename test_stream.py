import requests
import json
import sys

def test_stream():
    url = "http://127.0.0.1:8000/chat"
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }
    data = {
        "message": "What is 2+2? Please explain step by step."
    }
    
    print("Sending request...")
    response = requests.post(url, json=data, headers=headers, stream=True)
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 200:
        print("\nStreaming response:")
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = line[6:]
                    if data == '[DONE]':
                        print("\nStream complete")
                        break
                    try:
                        content = json.loads(data)
                        if 'content' in content:
                            print(content['content'], end='', flush=True)
                    except json.JSONDecodeError as e:
                        print(f"\nError parsing JSON: {e}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_stream() 