# AI Chatbot

A modern, responsive web-based AI chatbot interface powered by DeepSeek via OpenRouter. The interface features a sleek dark theme with a night mode aesthetic, real-time message streaming, and a beautiful user experience.

## 🌟 Key Features

### User Interface
- 🌙 Modern dark theme with night mode aesthetic
- 🎨 Beautiful UI with blur effects and gradients
- 📱 Fully responsive design for all devices
- ⚡ Fast and smooth animations
- 🔄 Auto-resizing input field
- ⌨️ Enter to send, Shift+Enter for new line
- 📱 Mobile-optimized with safe area support

### Chat Features
- 🤖 Powered by DeepSeek AI via OpenRouter
- 💬 Real-time message streaming
- 📝 Support for markdown formatting in messages
- 💻 Code block syntax highlighting
- 🔄 Dynamic message updates
- ⏳ Typing indicators
- ❌ Error handling and recovery

### Technical Features
- Real-time streaming responses
- Markdown support for rich text formatting
- Code block syntax highlighting
- Mobile-first responsive design
- iOS/Android safe area support
- Dynamic viewport handling
- Smooth animations and transitions
- Error handling and recovery
- Loading states and typing indicators

## 🚀 Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn
- OpenRouter API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-chatbot.git
   cd ai-chatbot
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Set up your environment variables:
   ```bash
   cp .env.example .env
   ```
   Then add your OpenRouter API key to the `.env` file:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   PORT=3000
   ```

4. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. Open your browser and navigate to `http://localhost:3000`

## 🛠️ Project Structure

```
ai-chatbot/
├── public/
│   ├── index.html      # Main HTML file
│   └── background.jpg  # Background image
├── src/
│   ├── api/           # API integration
│   ├── styles/        # CSS styles
│   └── utils/         # Utility functions
├── .env.example       # Example environment variables
├── package.json       # Project dependencies
└── README.md         # Project documentation
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | - |
| `PORT` | Server port | 3000 |

### UI Customization

The interface can be customized by modifying the CSS variables in `public/index.html`:

```css
:root {
    --primary-color: #007AFF;
    --primary-color-dark: rgba(0, 86, 204, 0.8);
    --bg-message-user: rgba(0, 122, 255, 0.7);
    --bg-message-bot: rgba(255, 255, 255, 0.15);
    --text-color: white;
    --border-color: rgba(255, 255, 255, 0.2);
    --error-color: rgba(255, 59, 48, 0.9);
}
```

## 📱 Mobile Support

The application is fully responsive and optimized for mobile devices:
- Safe area support for notched devices
- Touch-friendly interface
- Responsive layout
- Mobile-optimized input handling
- Dynamic viewport adjustments

## 🔒 Security

- API keys are stored securely in environment variables
- HTTPS support for production
- Input sanitization
- Error handling and recovery

## 🚀 Deployment

### Production Build
```bash
npm run build
# or
yarn build
```

### Deployment Options
- Vercel
- Netlify
- GitHub Pages
- Any static hosting service

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
- Built with modern web technologies
- Inspired by modern chat interfaces

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.
