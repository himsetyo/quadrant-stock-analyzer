# 🚀 Deployment Guide

Panduan untuk deploy Quadrant Stock Analyzer ke berbagai platform.

---

## 📦 Streamlit Cloud (Recommended)

Streamlit Cloud adalah cara termudah untuk deploy aplikasi Streamlit secara gratis.

### Prerequisites
- GitHub account
- Streamlit Cloud account (sign up di [share.streamlit.io](https://share.streamlit.io))

### Steps

1. **Push project ke GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/quadrant-stock-analyzer.git
   git push -u origin main
   ```

2. **Deploy di Streamlit Cloud**
   - Login ke [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Pilih repository: `yourusername/quadrant-stock-analyzer`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Done!**
   - Aplikasi akan tersedia di: `https://yourusername-quadrant-stock-analyzer.streamlit.app`
   - Auto-deploy setiap kali push ke GitHub

### Configuration

Jika perlu environment variables, buat file `.streamlit/secrets.toml`:

```toml
# .streamlit/secrets.toml
API_KEY = "your_api_key_here"
```

---

## 🐳 Docker Deployment

Deploy menggunakan Docker container.

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
# Build image
docker build -t quadrant-stock-analyzer .

# Run container
docker run -p 8501:8501 quadrant-stock-analyzer
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

Run with:
```bash
docker-compose up
```

---

## ☁️ Heroku Deployment

Deploy ke Heroku cloud platform.

### Prerequisites
- Heroku account
- Heroku CLI installed

### Setup Files

1. **Create `setup.sh`**
   ```bash
   mkdir -p ~/.streamlit/
   
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

2. **Create `Procfile`**
   ```
   web: sh setup.sh && streamlit run app.py
   ```

3. **Create `runtime.txt`**
   ```
   python-3.11.0
   ```

### Deploy

```bash
# Login to Heroku
heroku login

# Create app
heroku create quadrant-stock-analyzer

# Push to Heroku
git push heroku main

# Open app
heroku open
```

---

## 🌐 AWS EC2 Deployment

Deploy ke AWS EC2 instance.

### Launch EC2 Instance

1. Launch Ubuntu 22.04 instance
2. Configure security group (allow port 8501)
3. SSH to instance

### Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3.11 python3-pip -y

# Clone repository
git clone https://github.com/yourusername/quadrant-stock-analyzer.git
cd quadrant-stock-analyzer

# Install dependencies
pip3 install -r requirements.txt

# Run with nohup (background)
nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
```

### Using Nginx as Reverse Proxy

```bash
# Install Nginx
sudo apt install nginx -y

# Configure Nginx
sudo nano /etc/nginx/sites-available/streamlit
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔧 Environment Variables

Untuk production deployment, set environment variables:

```bash
# Streamlit configuration
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true

# Application settings
export APP_ENV=production
export LOG_LEVEL=INFO
```

---

## 📊 Monitoring

### Streamlit Cloud
- Built-in monitoring di dashboard
- View logs dan metrics

### Custom Deployment
- Use monitoring tools seperti:
  - **Prometheus** + **Grafana** untuk metrics
  - **ELK Stack** untuk logging
  - **Sentry** untuk error tracking

---

## 🔒 Security Best Practices

1. **HTTPS**: Always use HTTPS in production
2. **Authentication**: Implement user authentication jika diperlukan
3. **Rate Limiting**: Prevent abuse dengan rate limiting
4. **Input Validation**: Validate semua user inputs
5. **Secrets Management**: Jangan commit secrets ke Git

---

## 🚦 Health Check

Add health check endpoint untuk monitoring:

```python
# Add to app.py
import streamlit as st

@st.cache_data
def health_check():
    return {"status": "healthy", "version": "1.0"}
```

---

## 📈 Scaling

### Horizontal Scaling
- Deploy multiple instances
- Use load balancer (AWS ELB, Nginx)

### Vertical Scaling
- Increase instance size
- Optimize code performance

---

## 🔄 CI/CD Pipeline

Example GitHub Actions workflow:

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          python -m pytest tests/
      
      - name: Deploy to Streamlit Cloud
        # Streamlit Cloud auto-deploys on push
        run: echo "Deployed!"
```

---

## 📝 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Kill process on port 8501
lsof -ti:8501 | xargs kill -9
```

**Module not found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Memory issues:**
```bash
# Increase memory limit
streamlit run app.py --server.maxUploadSize=200
```

---

## 📞 Support

Jika ada masalah deployment:
- Check [Streamlit Documentation](https://docs.streamlit.io)
- Open issue di GitHub repository
- Contact: your.email@example.com

---

**Happy Deploying! 🚀**

