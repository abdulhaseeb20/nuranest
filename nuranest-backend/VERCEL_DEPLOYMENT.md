# 🚀 Vercel Deployment Guide for Nuranest Pregnancy AI API

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install with `npm i -g vercel`
3. **Git Repository**: Your code should be in a Git repository

## 🔧 Environment Variables

Before deploying, you need to set these environment variables in Vercel:

### Required Variables:
- `GROQ_API_KEY` - Your Groq API key for LLM access

### Optional Variables:
- `DEBUG` - Set to "true" for debug mode (default: false)
- `LOG_LEVEL` - Logging level (default: INFO)

## 🚀 Deployment Steps

### Method 1: Using Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from your backend directory**:
   ```bash
   cd nuranest-backend
   vercel
   ```

4. **Follow the prompts**:
   - Link to existing project or create new
   - Set environment variables when prompted

### Method 2: Using Vercel Dashboard

1. **Connect your Git repository** to Vercel
2. **Import the project** and select the `nuranest-backend` directory
3. **Set environment variables** in the Vercel dashboard
4. **Deploy automatically** on every push

## ⚙️ Configuration Files

The following files are configured for Vercel deployment:

- `vercel.json` - Vercel configuration
- `api/index.py` - Serverless function entry point
- `runtime.txt` - Python version specification
- `.vercelignore` - Files to exclude from deployment

## 🔍 Testing Your Deployment

After deployment, test your API:

1. **Health Check**: `GET https://your-app.vercel.app/`
2. **API Documentation**: `GET https://your-app.vercel.app/docs`
3. **Ask Question**: `POST https://your-app.vercel.app/api/v1/ai/ask`

## 📝 Example API Request

```bash
curl -X POST "https://your-app.vercel.app/api/v1/ai/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What foods should I avoid during pregnancy?"
  }'
```

## ⚠️ Important Notes

1. **Vector Database**: The `vectorstore_local` directory (22.4 MB) is included in deployment. Your AI will work in FULL MODE with document retrieval.

2. **Cold Starts**: Vercel functions have cold starts. The first request might be slower.

3. **Timeout Limits**: Vercel has timeout limits (10s for hobby plan, 60s for pro).

4. **Environment Variables**: Make sure to set `GROQ_API_KEY` in Vercel dashboard.

## 🐛 Troubleshooting

### Common Issues:

1. **Import Errors**: Make sure all dependencies are in `requirements.txt`
2. **Environment Variables**: Check that `GROQ_API_KEY` is set correctly
3. **Timeout Errors**: Consider optimizing your AI processing for faster responses
4. **Memory Issues**: Vercel has memory limits; consider using lighter models

### Debug Mode:

Set `DEBUG=true` in environment variables to get more detailed error messages.

## 📞 Support

If you encounter issues:
1. Check Vercel deployment logs
2. Verify environment variables are set correctly
3. Test locally first with `uvicorn app.main:app --reload` 