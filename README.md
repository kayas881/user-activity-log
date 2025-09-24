# User Activity Monitoring Tool

A Flask-based web GUI for monitoring system activity, processes, and user sessions.

## Features

- Real-time monitoring (users + processes)
- Log current activity snapshots
- Generate daily usage reports
- Check high resource usage alerts
- Show recent user session history

## Local Development

```bash
python app.py
```

Visit `http://localhost:5050` in your browser.

## Deploy to Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Login: `vercel login`
3. Deploy: `vercel --prod`

**Note:** Some system commands may not work in Vercel's serverless environment. The app includes error handling for these cases.

## Files

- `app.py` - Main Flask application for local development
- `api/index.py` - Serverless function for Vercel deployment
- `templates/` - HTML templates
- `vercel.json` - Vercel deployment configuration