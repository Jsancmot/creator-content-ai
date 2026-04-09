# Instagram Agent

Automated Instagram content workflow using AI agents, Google Drive, and Telegram.

## Description

This agent monitors a Google Drive folder for new images, processes them with AI (image editing + caption generation), uploads the results to an output folder, and sends notifications via Telegram.

## Features

- **Google Drive Integration**: Monitor input folder, download images, upload processed images
- **Image Editor Agent**: Edit images using AI via LiteLLM (Qwen model)
- **Caption Agent**: Generate Instagram captions using AI via LiteLLM (Groq/Llama model)
- **Telegram Notifications**: Send processed images with captions to your Telegram chat
- **Polling Scheduler**: Configurable interval for checking new images
- **Docker Support**: Fully containerized for easy deployment

## Environment Variables

### Required

| Variable | Description |
|----------|-------------|
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Google Drive service account credentials (JSON) |
| `GOOGLE_DRIVE_INPUT_FOLDER_ID` | ID of the Google Drive folder to monitor |
| `GOOGLE_DRIVE_OUTPUT_FOLDER_ID` | ID of the Google Drive folder for output |

### Optional - LiteLLM

| Variable | Description | Default |
|----------|-------------|---------|
| `LITELLM_API_KEY` | API key for LiteLLM | - |
| `LITELLM_BASE_URL` | Custom LiteLLM base URL | - |
| `IMAGE_MODEL` | Model for image editing | `qwen/qwen2-vl-7b-instruct` |
| `CAPTION_MODEL` | Model for caption generation | `groq/llama-3.3-70b-versatile` |

### Optional - Telegram

| Variable | Description |
|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token |
| `TELEGRAM_CHAT_ID` | Telegram chat ID to send notifications |

### Optional - Application

| Variable | Description | Default |
|----------|-------------|---------|
| `POLLING_INTERVAL_MINUTES` | Interval between polls | `5` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Quick Start

1. Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

2. Run with Docker:

```bash
docker-compose up -d
```

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python tests/test_credentials.py

# Run locally
python src/main.py
```

## Project Structure

```
instagram-agent/
├── src/
│   ├── agents/           # AI agents (image editor, caption)
│   ├── clients/          # Drive and Telegram clients
│   ├── scheduler/        # Polling scheduler
│   ├── utils/            # Utilities
│   └── main.py           # Entry point
├── config/
│   ├── settings.yaml     # Configuration
│   └── prompts/          # AI prompts
├── tests/                # Tests
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Deployment

This project is ready for deployment on Render with Docker. Set the environment variables in your Render dashboard and deploy using the Dockerfile.