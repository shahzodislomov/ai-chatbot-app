# 🚀 Deployment Guide

Deploy your AI chatbot to the cloud for free or cheap.

---

## Docker (Recommended)

### Prerequisites
- Docker & Docker Compose installed

### Local Deployment

```bash
# Start everything at once
docker-compose up -d

# Access at:
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# Ollama: http://localhost:11434

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

---

## Cloud Deployment

### Option 1: Railway.app (Easiest + Free)

**Cost:** Free tier available, pay-as-you-go after

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
cd ai-chatbot-app
railway init

# Deploy backend
cd backend
railway up

# Deploy frontend
cd ../frontend
railway up
```

**Features:**
- Auto-deploys on git push
- Free PostgreSQL/Redis
- Custom domains
- GitHub integration

[Railway Dashboard](https://railway.app)

---

### Option 2: Render.com

**Cost:** Free tier available

```bash
# Push to GitHub
git push origin main

# Connect on https://render.com
# Auto-deploys on push
```

**Manual Deploy:**
```bash
# Build docker image
docker build -t chatbot-backend ./backend

# Push to Docker Hub
docker tag chatbot-backend USERNAME/chatbot-backend
docker push USERNAME/chatbot-backend

# Deploy on Render with Docker image
```

---

### Option 3: Hugging Face Spaces (Free GPU!)

**Cost:** Free with GPU option

```bash
# Create repo on https://huggingface.co/spaces

# Push code
git push huggingface main

# App deploys automatically
```

**Note:** Great for demoing, limited CPU for production

---

### Option 4: DigitalOcean App Platform

**Cost:** $7-50/month

```bash
# Deploy via web console at https://cloud.digitalocean.com/apps

# Or use doctl CLI:
doctl apps create --spec app.yaml

# Use this app.yaml:
```

```yaml
name: chatbot
services:
  - name: backend
    github:
      repo: your-username/ai-chatbot-app
      branch: main
    build_command: cd backend && pip install -r requirements.txt
    run_command: cd backend && python main.py
    http_port: 8000

  - name: frontend
    github:
      repo: your-username/ai-chatbot-app
      branch: main
    build_command: cd frontend && npm install && npm run build
    run_command: cd frontend && npm run preview
    http_port: 5173
```

---

### Option 5: AWS (Production-Grade)

**Cost:** $20-100/month

#### Using ECS + Fargate

```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure

# Create ECR repository
aws ecr create-repository --repository-name chatbot-backend
aws ecr create-repository --repository-name chatbot-frontend

# Build and push Docker images
docker build -t chatbot-backend ./backend
docker tag chatbot-backend:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/chatbot-backend:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/chatbot-backend:latest

# Same for frontend
docker build -t chatbot-frontend ./frontend
docker tag chatbot-frontend:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/chatbot-frontend:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/chatbot-frontend:latest

# Create ECS cluster, task definitions, and services via AWS Console
# (Or use CloudFormation template)
```

---

### Option 6: Self-Hosted (VPS)

**Cost:** $5-20/month

#### Using Linode (example)

```bash
# 1. Create Linode instance (Ubuntu 22.04)
# 2. SSH into server
ssh root@YOUR_IP

# 3. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 4. Clone repo
git clone https://github.com/your-username/ai-chatbot-app.git
cd ai-chatbot-app

# 5. Update environment
nano .env
# Set FRONTEND_URL=https://your-domain.com
# Set OLLAMA_BASE_URL=http://ollama:11434

# 6. Deploy
docker-compose -f docker-compose.prod.yml up -d

# 7. Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com
# Copy certs to ./ssl/
```

**VPS Providers (Cheapest):**
- Linode: $5/month (1GB RAM)
- DigitalOcean Droplets: $4-6/month
- Vultr: $2.50/month (limited)
- Hetzner: $4/month (EU)

---

## Environment Variables for Production

### Backend (.env)

```env
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=mistral
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=https://your-domain.com
DATABASE_URL=postgresql://user:pass@db:5432/chatbot
```

### Frontend (.env)

```env
VITE_API_URL=https://api.your-domain.com
```

---

## Database Setup (Optional)

For production, use PostgreSQL instead of SQLite:

```bash
# Create db service in docker-compose.yml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: chatbot
      POSTGRES_USER: chatbot
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## Domain & SSL

### Using Cloudflare (Free)

1. Buy domain (Namecheap, GoDaddy, etc.)
2. Add to Cloudflare (free account)
3. Use Cloudflare DNS
4. Enable "Full" SSL/TLS (free)
5. Set A record to your server IP

### Using Let's Encrypt (Free)

```bash
# Auto-renew certificates
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Monitoring & Logging

### Using ELK Stack (Free, Self-Hosted)

```docker-compose.yml
elk:
  image: sebp/elk:latest
  ports:
    - "5601:5601"  # Kibana
  volumes:
    - elk_data:/var/lib/elasticsearch
```

### Using Sentry (Error Tracking)

```bash
# Install
pip install sentry-sdk

# In backend/main.py
import sentry_sdk
sentry_sdk.init(
    dsn="https://your-sentry-dsn",
    traces_sample_rate=0.1
)
```

### Using Datadog (Monitoring)

Sign up at https://www.datadoghq.com/ (free tier available)

---

## CI/CD (GitHub Actions)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: |
          npm install -g @railway/cli
          railway up

      - name: Deploy Frontend
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
        run: |
          npm install -g vercel
          vercel --token $VERCEL_TOKEN
```

---

## Cost Breakdown

| Service | Monthly | Best For |
|---------|---------|----------|
| Railway | $0-20 | Getting started |
| Render | $0-20 | Small projects |
| Linode VPS | $5+ | Full control |
| DigitalOcean | $5+ | Reliability |
| AWS | $50+ | Scale |
| Heroku | $7-50 | Simplicity (pricey) |

**Recommendation:** Start with **Railway** (free), move to **VPS** when you need scale.

---

## Performance Optimization

### Backend
```python
# In main.py
# Enable caching
from fastapi_cache2 import FastAPICache2
FastAPICache2.init(RedisBackend(...), prefix="chatbot")
```

### Frontend
```bash
# Optimize build
npm run build
# Check bundle size
npm install -g webpack-bundle-analyzer
```

### Ollama
```bash
# Use smaller model for faster responses
ollama pull neural-chat  # Smaller, faster
ollama pull mistral      # Balanced
ollama pull mistral-large # Better quality, slower
```

---

## Troubleshooting

**Backend connection refused**
```bash
# Check if backend is running
curl http://localhost:8000/

# Check logs
docker-compose logs backend
```

**Ollama GPU not detected**
```bash
# Install NVIDIA Container Runtime
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-docker2
```

**Memory issues**
```bash
# Check resource usage
docker stats

# Increase Docker memory
# Edit Docker Desktop settings or daemon.json
```

---

## Backup & Recovery

```bash
# Backup database
docker-compose exec db pg_dump chatbot > backup.sql

# Backup Ollama models
docker cp chatbot_ollama_1:/root/.ollama ./ollama-backup

# Restore
docker-compose exec db psql chatbot < backup.sql
```

---

Enjoy your deployed chatbot! 🎉
