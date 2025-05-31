import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    print("❌ No API key found in environment variables")
    print("Please create a .env file with: OPENROUTER_API_KEY=your-key-here")
    exit(1)

print(f"✅ Using OpenRouter API key: {API_KEY[:8]}...")

def test_api():
    """Test the OpenRouter API connection and DeepSeek model"""
    print("\n🚀 Testing OpenRouter API...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "AI Chatbot Test"
    }
    
    # Test payload
    payload = {
        "model": "deepseek/deepseek-r1",
        "messages": [
            {
                "role": "system", 
                "content": "You are a helpful AI assistant. Respond concisely."
            },
            {
                "role": "user", 
                "content": "Hello! Please respond with a simple greeting."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 100,
        "stream": False
    }
    
    try:
        print("Making API request...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if "error" in data:
                print(f"❌ API Error: {data['error']['message']}")
                return False
            
            if "choices" in data and data["choices"]:
                response_text = data["choices"][0]["message"]["content"]
                print(f"✅ Success! AI Response: {response_text}")
                return True
            else:
                print("❌ No response content found")
                return False
                
        elif response.status_code == 401:
            print("❌ Authentication failed - check your API key")
            return False
        elif response.status_code == 429:
            print("❌ Rate limit exceeded")
            return False
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_local_app():
    """Test the local FastAPI app"""
    print("\n🔍 Testing local FastAPI app...")
    
    try:
        # Test health endpoint
        health_response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print("✅ Health check passed")
            print(f"   Status: {health_data.get('status')}")
            print(f"   Has API Key: {health_data.get('has_api_key')}")
            
            # Test static files
            try:
                static_response = requests.get("http://127.0.0.1:8000/", timeout=5)
                if static_response.status_code == 200:
                    print("✅ Frontend accessible")
                else:
                    print(f"❌ Frontend error: {static_response.status_code}")
            except:
                print("❌ Frontend not accessible")
            
            # Test chat endpoint with streaming
            print("Testing chat endpoint...")
            chat_response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"message": "Hello from test!"},
                timeout=30,
                stream=True
            )
            
            if chat_response.status_code == 200:
                print("✅ Chat endpoint working (streaming response)")
                # Read a few chunks to verify streaming
                chunk_count = 0
                for chunk in chat_response.iter_content(chunk_size=1024):
                    if chunk:
                        chunk_count += 1
                        if chunk_count >= 3:  # Read first few chunks
                            break
                print(f"   Received {chunk_count} chunks")
            else:
                print(f"❌ Chat endpoint error: {chat_response.status_code}")
                print(f"   Response: {chat_response.text}")
        else:
            print(f"❌ Health check failed: {health_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("ℹ️ Local app not running")
        print("  To test: run 'python app.py' in another terminal")
    except Exception as e:
        print(f"❌ Error testing local app: {str(e)}")

def test_streaming_api():
    """Test streaming functionality"""
    print("\n🌊 Testing streaming API...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "AI Chatbot Test - Streaming"
    }
    
    payload = {
        "model": "deepseek/deepseek-r1",
        "messages": [
            {
                "role": "system", 
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user", 
                "content": "Count from 1 to 5, with each number on a new line."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 100,
        "stream": True
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            stream=True,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Streaming API working")
            chunk_count = 0
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        chunk_count += 1
                        if chunk_count <= 5:  # Show first 5 chunks
                            print(f"   Chunk {chunk_count}: {line_str[:50]}...")
                        if chunk_count >= 10:  # Stop after 10 chunks
                            break
            print(f"   Total chunks processed: {chunk_count}")
        else:
            print(f"❌ Streaming failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Streaming test error: {str(e)}")

def check_static_files():
    """Check if static files exist"""
    print("\n📁 Checking static files...")
    
    static_files = {
        "public/background.jpg": "Background image",
        "public/index.html": "Frontend HTML (optional - can be in root)",
        "index.html": "Frontend HTML (alternative location)"
    }
    
    for file_path, description in static_files.items():
        if os.path.exists(file_path):
            print(f"✅ {description}: {file_path}")
        else:
            if file_path == "public/background.jpg":
                print(f"❌ {description}: {file_path} (REQUIRED)")
            else:
                print(f"ℹ️ {description}: {file_path} (optional)")
    
    # Check if public directory exists
    if not os.path.exists("public"):
        print("ℹ️ Creating public directory...")
        os.makedirs("public", exist_ok=True)
        print("✅ Public directory created")

if __name__ == "__main__":
    print("OpenRouter API Test Suite")
    print("=" * 40)
    
    # Check static files first
    check_static_files()
    
    # Test basic API
    api_success = test_api()
    
    if api_success:
        # Test streaming
        test_streaming_api()
        
        # Test local app
        test_local_app()
        
        print("\n" + "=" * 40)
        print("✅ All tests completed!")
        print("\nNext steps:")
        print("1. Ensure your .env file has your API key")
        print("2. Add background.jpg to the static/ folder")
        print("3. Run: python app.py")
        print("4. Open: http://127.0.0.1:8000")
        print("5. Start chatting!")
    else:
        print("\n" + "=" * 40)
        print("❌ Basic API test failed!")
        print("\nPlease check:")
        print("1. Your API key is correct in the .env file")
        print("2. You have sufficient credits")
        print("3. Your internet connection")
        print("4. The model 'deepseek/deepseek-r1' is available")