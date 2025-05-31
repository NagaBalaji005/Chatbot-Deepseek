# AI Chatbot

A modern, responsive AI chatbot powered by DeepSeek via OpenRouter. Built with FastAPI and vanilla JavaScript, featuring a beautiful UI and real-time streaming responses.

## 🌟 Features

### Frontend
- 🌙 Modern dark theme with night mode aesthetic
- 📱 Fully responsive design for all devices
- 💬 Real-time message streaming
- ⌨️ Support for markdown formatting in messages
- ⚡ Fast and smooth animations
- 🔄 Auto-resizing input field
- ⌨️ Enter to send, Shift+Enter for new line
- 📱 Mobile-optimized with safe area support
- 🎨 Beautiful UI with blur effects and gradients
- 🔄 Service worker for offline support

### Backend
- 🚀 FastAPI for high performance
- 💨 Real-time streaming responses
- 🔒 Secure API handling
- ⚡ Async request processing
- 🛡️ Comprehensive error handling
- 🔄 CORS support
- 📝 Environment variable validation

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- OpenRouter API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-chatbot.git
   cd ai-chatbot
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   ```bash
   cp .env.example .env
   ```
   Then add your OpenRouter API key to the `.env` file:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   ```

4. Run the development server:
   ```bash
   uvicorn api.chat:app --reload
   ```

5. Open your browser and navigate to `http://localhost:8000`

## 🛠️ Project Structure

```
Chatbot/
├── public/                    # Static files
│   ├── index.html            # Main HTML file
│   ├── background.jpg        # Background image
│   ├── favicon.ico          # Favicon
│   └── sw.js                # Service worker
│
├── api/                      # Backend API
│   ├── chat.py              # Python chat endpoint
│   └── runtime.txt          # Python runtime version
│
├── config.py                 # Configuration file
├── requirements.txt          # Python dependencies
├── test_api.py              # API tests
├── test_stream.py           # Stream tests
├── README.md                # Project documentation
├── .gitignore               # Git ignore rules
└── vercel.json              # Vercel configuration
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | Yes |

### API Endpoints

- `GET /`: Frontend interface
- `POST /api/chat`: Chat endpoint
- `GET /health`: Health check
- `GET /api/info`: API information

## 📱 Mobile Support

The application is fully responsive and optimized for mobile devices:
- Safe area support for notched devices
- Touch-friendly interface
- Responsive layout
- Mobile-optimized input handling
- Dynamic viewport adjustments
- Service worker for offline support

## 🚀 Deployment

### Vercel Deployment

1. Fork this repository
2. Create a new project on Vercel
3. Connect your repository
4. Add environment variables in Vercel dashboard
5. Deploy!

### Other Platforms

The application can be deployed on any platform that supports Python/FastAPI applications:
- Heroku
- DigitalOcean
- AWS
- Google Cloud
- Azure

## 🧪 Testing

Run the test suite:
```bash
python -m pytest test_api.py test_stream.py
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Powered by [DeepSeek](https://deepseek.com) via [OpenRouter](https://openrouter.ai)
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend built with vanilla JavaScript

- Made by naga balaji
- linkedin - [www.linkedin.com/in/adapala-naga-balaji-339b4131a]
