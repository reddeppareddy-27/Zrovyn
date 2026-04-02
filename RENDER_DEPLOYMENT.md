# Render Deployment Guide

This guide walks you through deploying the Finance Dashboard Backend to Render.

## Prerequisites

- GitHub account with the repository pushed
- Render account (create at https://render.com)
- PostgreSQL 15+ (Render provides)

## Step 1: Create a Render Account

1. Go to https://render.com
2. Sign up or log in with GitHub (recommended for easier integration)
3. Verify your email

## Step 2: Create a PostgreSQL Database

1. From Render dashboard, click **New +**
2. Select **PostgreSQL**
3. Configure:
   - **Name**: `finance-postgres` (or your preference)
   - **Database**: `backend_intern`
   - **User**: `backend_intern`
   - **Region**: Choose closest to you
   - **PostgreSQL Version**: 15
   - **Plan**: Free starter tier (2 connections, 256MB)
4. Click **Create Database**
5. Copy the database URL (format: `postgresql://user:password@host:5432/database`)
   - Save this for the next step

## Step 3: Create a Web Service

1. From Render dashboard, click **New +**
2. Select **Web Service**
3. Connect your GitHub repository:
   - Click **Connect GitHub account** if needed
   - Select your `finance_backend` repository
   - Authorize Render to access it
4. Configure the service:
   - **Name**: `finance-backend` (or your preference)
   - **Region**: Same as database
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn finance_backend.wsgi:application`
   - **Plan**: Free (optional $5/month credit)
5. Click **Advanced** and add Environment Variables:

## Step 4: Add Environment Variables

1. In the Web Service settings, click **Add Environment Variable** for each:

   ```
   DEBUG=False
   SECRET_KEY=<generate-at-https://djecrety.ir/>
   ALLOWED_HOSTS=<your-render-url>.onrender.com
   DB_ENGINE=django.db.backends.postgresql
   DATABASE_URL=<copy-from-step-2>
   ```

   Or individually:
   ```
   DB_NAME=backend_intern
   DB_USER=backend_intern
   DB_PASSWORD=<password-from-database>
   DB_HOST=<host-from-database-url>
   DB_PORT=5432
   CORS_ALLOWED_ORIGINS=https://<your-frontend-domain>.com
   ```

2. Click **Create Web Service**

## Step 5: Monitor Deployment

1. Render will automatically:
   - Pull from GitHub
   - Run your build command
   - Run migrations
   - Start the web service
2. Watch the **Logs** tab for progress
3. Once "Build successful" appears, your API is deployed!

## Step 6: Access Your API

Your API is available at: `https://<service-name>.onrender.com`

Test it:
```bash
curl https://<service-name>.onrender.com/api/v1/roles/
```

## Troubleshooting

### Build Fails on `collectstatic`
- Ensure `STATIC_ROOT = BASE_DIR / 'staticfiles'` in settings.py ✓
- Ensure WhiteNoise is installed ✓
- Both are already configured

### Database Connection Error
- Verify `DATABASE_URL` is correctly set
- Check database status in Render dashboard (should show "Available")
- Ensure migrations ran (check logs)

### 502 Bad Gateway
- Check logs for application errors
- Ensure `SECRET_KEY` is set (not the default dev key)
- Verify `ALLOWED_HOSTS` includes your Render domain

### Static Files Not Loading
- WhiteNoise is configured to serve static files ✓
- Build command must include `collectstatic --noinput` ✓

## Auto-Deployment

Rendered automatically redeploys when you:
- Push to the `main` branch
- Update environment variables
- Restart the service

## Commands for Manual Testing

After deployment, test these endpoints:

```bash
# Get all roles
curl https://<your-url>.onrender.com/api/v1/roles/

# Get all users
curl https://<your-url>.onrender.com/api/v1/users/

# Get financial records (requires auth)
curl -H "Authorization: Token <your-token>" \
  https://<your-url>.onrender.com/api/v1/financial-records/
```

## Production Checklist

Before final submission:
- [ ] `DEBUG=False` in production
- [ ] `SECRET_KEY` is generated (not default)
- [ ] `ALLOWED_HOSTS` includes your Render URL
- [ ] Database is created and connected
- [ ] Migrations completed successfully
- [ ] API responds to test requests
- [ ] Static files load (CSS, etc.)
- [ ] CORS configured for frontend domain

## Files Added/Modified for Deployment

- `requirements.txt` - Added gunicorn, whitenoise, psycopg2-binary
- `finance_backend/settings.py` - Added security settings, WhiteNoise, production logging
- `Procfile` - Release and web command configuration
- `render.yaml` - Alternative Render configuration (optional)
- `build.sh` - Build script (optional, Render uses Procfile)
- `.env.example` - Updated with Render environment variable examples

## Support

For issues:
1. Check Render logs (Services → Logs)
2. Review Django debug messages
3. Verify all environment variables are set
4. Check database status in Render dashboard
