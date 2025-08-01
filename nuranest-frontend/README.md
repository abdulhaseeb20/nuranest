# Nuranest Frontend

A beautiful, modern React frontend for the Nuranest Pregnancy Health AI Assistant. This application provides an intuitive chat interface for users to ask pregnancy-related health questions and receive AI-powered responses.

## 🚀 Features

- **Modern UI/UX**: Beautiful, responsive design with smooth animations
- **Real-time Chat**: Interactive chat interface with the AI assistant
- **Connection Status**: Real-time API connection monitoring
- **Suggested Questions**: Quick access to common pregnancy questions
- **Loading States**: Smooth loading animations and feedback
- **Error Handling**: Comprehensive error handling and user feedback
- **Mobile Responsive**: Optimized for all device sizes
- **Accessibility**: Built with accessibility best practices

## 🛠️ Tech Stack

- **React 18**: Modern React with hooks
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Smooth animations and transitions
- **Axios**: HTTP client for API communication
- **Lucide React**: Beautiful icons
- **React Hot Toast**: Toast notifications
- **Vite**: Fast build tool (for development)

## 📦 Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd nuranest-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open your browser:**
   Navigate to `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000

# Optional: Custom API endpoint for production
# REACT_APP_API_URL=https://your-api-domain.com
```

### Backend Connection

Make sure your Nuranest backend is running on `http://localhost:8000` (or update the `REACT_APP_API_URL` accordingly).

## 🏗️ Project Structure

```
nuranest-frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Header.js
│   │   ├── WelcomeMessage.js
│   │   ├── ChatMessage.js
│   │   ├── LoadingMessage.js
│   │   └── QuestionInput.js
│   ├── services/
│   │   └── api.js
│   ├── App.js
│   ├── index.js
│   └── index.css
├── package.json
├── tailwind.config.js
└── README.md
```

## 🎨 Components

### Header
- Logo and branding
- Connection status indicator
- Navigation links

### WelcomeMessage
- Introduction and features
- Medical disclaimer
- Feature highlights

### ChatMessage
- User and AI message display
- Timestamp and confidence scores
- Processing time information

### LoadingMessage
- Animated loading indicator
- "AI is thinking" message

### QuestionInput
- Text input for questions
- Suggested questions buttons
- Voice input (placeholder)
- Connection status

## 🔌 API Integration

The frontend connects to the Nuranest backend API with the following endpoints:

- `GET /` - Health check
- `POST /api/v1/ai/ask` - Ask pregnancy health questions
- `GET /docs` - API documentation

## 🚀 Deployment

### Vercel Deployment

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Build the project:**
   ```bash
   npm run build
   ```

3. **Deploy to Vercel:**
   ```bash
   vercel
   ```

4. **Set environment variables in Vercel dashboard:**
   - `REACT_APP_API_URL`: Your deployed backend URL

### Other Platforms

The app can be deployed to any static hosting platform:
- Netlify
- GitHub Pages
- AWS S3
- Firebase Hosting

## 🎯 Usage

1. **Start the application** and wait for the connection to establish
2. **Ask questions** about pregnancy health using the chat interface
3. **Use suggested questions** for quick access to common topics
4. **View confidence scores** and processing times for AI responses
5. **Clear chat** to start a new conversation

## 🔒 Security

- All API calls are made over HTTPS in production
- No sensitive data is stored locally
- Medical disclaimer is prominently displayed
- Users are advised to consult healthcare professionals

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support or questions:
- Check the API documentation at `/docs`
- Review the backend logs for errors
- Ensure the backend service is running
- Verify environment variables are set correctly

## 🔄 Updates

To update the frontend:

1. Pull the latest changes
2. Install new dependencies: `npm install`
3. Test the application: `npm start`
4. Deploy updates: `npm run build && vercel --prod`

---

**Note**: This frontend is designed to work with the Nuranest backend API. Make sure the backend is properly configured and running before using the frontend. 