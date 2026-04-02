# Deployment Guide

This guide covers deploying the Finance Backend to production environments.

## Pre-Deployment Checklist

- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` is strong and kept secure
- [ ] `ALLOWED_HOSTS` is configured
- [ ] Database is configured for production
- [ ] Static files collection is configured
- [ ] Logging is configured
- [ ] Error tracking (e.g., Sentry) is set up
- [ ] All tests pass
- [ ] Database backups are configured

## Environment Setup

### Production .env Variables

```
DEBUG=False
SECRET_KEY=<strong-random-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_ENGINE=django.db.backends.postgresql
DB_NAME=finance_db_prod
DB_USER=postgres_user
DB_PASSWORD=<secure-password>
DB_HOST=<db-host>
DB_PORT=5432

CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## Deployment Options

### Option 1: Traditional Server (Ubuntu/Debian)

#### 1. Install Dependencies

```bash
sudo apt-get update
sudo apt-get install python3 python3-venv postgresql postgresql-contrib nginx supervisor
```

#### 2. Create Application User

```bash
sudo useradd -m -s /bin/bash finance_app
sudo su - finance_app
```

#### 3. Clone Repository and Setup

```bash
cd /home/finance_app
git clone <repository> finance_backend
cd finance_backend

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. Configure Django

```bash
cp .env.example .env
# Edit .env with production settings
python manage.py migrate
python manage.py collectstatic --noinput
```

#### 5. Setup Gunicorn

Install Gunicorn:
```bash
pip install gunicorn
```

Create `gunicorn_config.py`:
```python
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
```

#### 6. Configure Supervisor

Create `/etc/supervisor/conf.d/finance_backend.conf`:
```ini
[program:finance_backend]
directory=/home/finance_app/finance_backend
command=/home/finance_app/finance_backend/venv/bin/gunicorn -c gunicorn_config.py finance_backend.wsgi:application
user=finance_app
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/finance_app/logs/gunicorn.log
```

Start Supervisor:
```bash
sudo systemctl restart supervisor
```

#### 7. Configure Nginx

Create `/etc/nginx/sites-available/finance_backend`:
```nginx
upstream finance_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://finance_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/finance_app/finance_backend/staticfiles/;
    }

    location /media/ {
        alias /home/finance_app/finance_backend/media/;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/finance_backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 8. SSL Certificate (Let's Encrypt)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Option 2: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "finance_backend.wsgi:application"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: finance_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             gunicorn -b 0.0.0.0:8000 finance_backend.wsgi:application"
    environment:
      DEBUG: 'False'
      DB_HOST: db
      DB_NAME: finance_db
      DB_USER: postgres
      DB_PASSWORD: postgres
    ports:
      - "8000:8000"
    depends_on:
      - db

volumes:
  postgres_data:
```

Deploy:
```bash
docker-compose up -d
```

### Option 3: Heroku Deployment

Create `Procfile`:
```
web: gunicorn finance_backend.wsgi:application --log-file -
release: python manage.py migrate
```

Create `runtime.txt`:
```
python-3.10.0
```

Deploy:
```bash
heroku login
heroku create finance-backend
heroku addons:create heroku-postgresql:standard-0
git push heroku main
heroku run python manage.py migrate
```

### Option 4: AWS Elastic Beanstalk

Create `.ebextensions/django.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: finance_backend.wsgi:application
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: /var/app/current:$PYTHONPATH
  aws:autoscaling:launchconfiguration:
    IamInstanceProfile: aws-elasticbeanstalk-ec2-role

commands:
  01_migrate:
    command: "python manage.py migrate"
    leader_only: true
  02_collectstatic:
    command: "python manage.py collectstatic --noinput"
```

Deploy:
```bash
eb create finance-backend --instance-type t3.micro
eb deploy
```

## Post-Deployment Steps

1. **Database Backup**
   ```bash
   pg_dump -U postgres finance_db > backup.sql
   ```

2. **Monitoring Setup**
   - Install and configure Sentry for error tracking
   - Set up log aggregation (CloudWatch, ELK)
   - Configure health checks

3. **Performance Optimization**
   - Enable GZip compression in Nginx
   - Configure caching headers
   - Set up CDN for static files

4. **Security Hardening**
   - Enable HTTPS/TLS
   - Set security headers (HSTS, X-Frame-Options, etc.)
   - Regular security updates

5. **Automated Backups**
   - Configure daily database backups
   - Test backup restoration

## Scaling Strategies

### Horizontal Scaling
- Run multiple Gunicorn workers
- Use load balancer (Nginx, AWS ELB)
- Database read replicas for high read traffic

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize database queries
- Implement caching layer (Redis)

### Database Optimization
- Index frequently queried columns
- Optimize slow queries
- Consider database sharding for large datasets

## Monitoring and Maintenance

### Log Monitoring
```bash
# View Gunicorn logs
tail -f /home/finance_app/logs/gunicorn.log

# View Django logs
tail -f /home/finance_app/finance_backend/logs/debug.log
```

### Health Checks
```bash
curl http://localhost:8000/admin/
```

### Database Maintenance
```bash
# Analyze and vacuum
python manage.py dbshell
VACUUM ANALYZE;
```

## Rollback Procedures

1. **Keep Previous Release**
   ```bash
   git tag releases/v1.0.0
   git push origin releases/v1.0.0
   ```

2. **Quick Rollback**
   ```bash
   git revert <commit-hash>
   git push origin main
   # Redeploy
   ```

3. **Database Rollback**
   ```bash
   python manage.py migrate <app> <migration-number>
   ```

## Common Issues and Solutions

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic --noinput` and check Nginx configuration

### Issue: Database connection timeout
**Solution**: Increase connection pool size, check network connectivity

### Issue: High memory usage
**Solution**: Reduce Gunicorn workers, optimize database queries, implement caching

### Issue: Slow API responses
**Solution**: Check database indexes, profile slow queries, implement pagination

## Additional Resources

- [Django Deployment Documentation](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PostgreSQL Performance Tips](https://wiki.postgresql.org/wiki/Performance_Optimization)
