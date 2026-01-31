# IPO Monitor - GitHub Actions Automation Setup Guide

## 📋 Overview
This guide will help you set up automated daily IPO monitoring using GitHub Actions. The workflow runs every day at 9:00 AM Dubai time (5:00 AM UTC) and sends email notifications for IPOs with offer amounts exceeding $200 million.

## 🚀 Quick Setup Steps

### 1. Create a New GitHub Repository

1. Go to https://github.com/new
2. Create a repository named `ipo-monitor` (or any name you prefer)
3. Make it **Public** or **Private** (your choice)
4. Initialize with a README (optional)
5. Click "Create repository"

### 2. Upload Files to Repository

Upload these files to your repository:

```
ipo-monitor/
├── .github/
│   └── workflows/
│       └── ipo_monitor.yml
├── ipo_monitor.py
└── README.md (this file)
```

**Option A: Using GitHub Web Interface**
1. Click "Add file" → "Upload files"
2. Create the folder structure by typing `.github/workflows/ipo_monitor.yml` in the filename
3. Upload both files
4. Commit changes

**Option B: Using Git CLI**
```bash
git clone https://github.com/YOUR_USERNAME/ipo-monitor.git
cd ipo-monitor

# Create directory structure
mkdir -p .github/workflows

# Copy your files
cp ipo_monitor.yml .github/workflows/
cp ipo_monitor.py .

# Commit and push
git add .
git commit -m "Add IPO monitoring automation"
git push
```

### 3. Configure GitHub Secrets

You need to add three secrets to your repository:

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

Add these three secrets:

| Secret Name | Value | Example |
|-------------|-------|---------|
| `MAIL_PASS` | Your Gmail App Password | `abcd efgh ijkl mnop` |
| `EMAIL_FROM` | Sender email address | `ibrahimkhanik9797@gmail.com` |
| `EMAIL_TO` | Recipient email address | `ibrahim.786.ik09@gmail.com` |

#### 🔐 How to Generate Gmail App Password:

1. Go to your Google Account: https://myaccount.google.com/
2. Enable 2-Step Verification if not already enabled:
   - Go to **Security** → **2-Step Verification**
   - Follow the setup process
3. Generate an App Password:
   - Go to **Security** → **2-Step Verification** → **App passwords**
   - Or directly: https://myaccount.google.com/apppasswords
   - Select app: **Mail**
   - Select device: **Other (Custom name)** → Type "IPO Monitor"
   - Click **Generate**
   - Copy the 16-character password (it will look like: `abcd efgh ijkl mnop`)
   - Use this as your `MAIL_PASS` secret (you can include or remove spaces)

### 4. Enable GitHub Actions

1. Go to your repository
2. Click on the **Actions** tab
3. If prompted, click **"I understand my workflows, go ahead and enable them"**

### 5. Test the Workflow Manually

Before waiting for the scheduled run, test it manually:

1. Go to **Actions** tab
2. Click on **"Daily IPO Monitor"** workflow
3. Click **"Run workflow"** → **"Run workflow"** button
4. Wait for the workflow to complete (usually 30-60 seconds)
5. Check your email for the notification

## 📅 Schedule Details

- **Scheduled Time**: 9:00 AM Dubai Time (UTC+4)
- **Cron Expression**: `0 5 * * *` (5:00 AM UTC)
- **Frequency**: Daily
- **Manual Trigger**: Available via "Run workflow" button

## 📧 Email Notifications

You'll receive one of three types of emails:

### 1. **IPOs Found** 🔔
```
Subject: 🔔 IPO Monitor - 2 Ticker(s) Found

IPO tickers with offer amount > $200M today:

• TICKER1
• TICKER2
```

### 2. **No Large IPOs** ✓
```
Subject: ✓ IPO Monitor - No Large IPOs Today

No IPOs with offer amount above $200M were found for today.
```

### 3. **Error Occurred** ❌
```
Subject: ❌ IPO Monitor - Error Occurred

The IPO monitoring script encountered an error:

[Error details]

Please check the logs.
```

## 🔍 Viewing Workflow Logs

1. Go to **Actions** tab in your repository
2. Click on the latest workflow run
3. Click on the **"monitor-ipos"** job
4. Expand each step to view detailed logs

Example log output:
```
============================================================
IPO Monitor Started
============================================================
Current time (Dubai): 2026-01-31 09:00:00 GST
Current time (Eastern): 2026-01-31 00:00:00 EST
Checking IPOs for date: 01/31/2026
Fetching IPO data from NASDAQ API...
Successfully fetched 5 priced IPOs
Ticker: EXAMPLE, Offer Amount: $250,000,000
  ✓ Qualified: EXAMPLE ($250,000,000)
Total qualified IPOs: 1
✓ Email sent successfully
============================================================
IPO Monitor Completed Successfully
============================================================
```

## 🧪 Testing & Verification

### Method 1: Screen Recording
1. Navigate to **Actions** tab
2. Click **"Run workflow"**
3. Record the screen showing:
   - Workflow starting
   - Workflow completing successfully (green checkmark)
   - Email arriving in your inbox

### Method 2: Provide Repository Access
1. Make your repository **Public**, or
2. Add reviewer as a collaborator:
   - Go to **Settings** → **Collaborators**
   - Click **Add people**
   - Enter their GitHub username

### Method 3: Share Logs & Screenshots
1. Take screenshots of:
   - Successful workflow run (green checkmark)
   - Workflow logs showing execution
   - Email received in your inbox
2. Compile into a PDF or document

## 🛠️ Troubleshooting

### Common Issues:

#### 1. "SMTP Authentication Failed"
- **Solution**: Verify your Gmail App Password is correct
- Make sure 2-Step Verification is enabled on your Google account
- Generate a new App Password and update the `MAIL_PASS` secret

#### 2. "Workflow doesn't run at scheduled time"
- **Solution**: GitHub Actions scheduled workflows can have up to 15-minute delays
- The first scheduled run might not occur immediately after setup
- Manual testing always works instantly

#### 3. "No IPO data retrieved"
- **Solution**: This is normal on days with no IPOs
- The NASDAQ API might be temporarily down
- Check the logs to see the actual API response

#### 4. "Python import errors"
- **Solution**: All dependencies are installed in the workflow
- Check the "Install dependencies" step logs
- The workflow uses Python 3.10 by default

#### 5. "Secrets not found"
- **Solution**: Make sure secrets are added at repository level, not environment level
- Secret names are case-sensitive: use `MAIL_PASS`, `EMAIL_FROM`, `EMAIL_TO`

## 📊 Monitoring & Maintenance

### View Workflow History
- Go to **Actions** tab to see all past runs
- Each run shows success/failure status
- Logs are retained for 90 days by default

### Update Email Recipients
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Edit the `EMAIL_TO` secret
3. Next run will use the new email

### Modify Schedule
1. Edit `.github/workflows/ipo_monitor.yml`
2. Change the cron expression (current: `0 5 * * *`)
3. Commit changes

Cron examples:
- `0 5 * * *` = 5:00 AM UTC daily (9:00 AM Dubai)
- `0 6 * * *` = 6:00 AM UTC daily (10:00 AM Dubai)
- `0 14 * * 1-5` = 2:00 PM UTC weekdays only

### Change IPO Threshold
1. Edit `ipo_monitor.py`
2. Find line: `if offer_amount > 200_000_000:`
3. Change `200_000_000` to desired amount (in USD)
4. Commit changes

## 📝 File Descriptions

### `.github/workflows/ipo_monitor.yml`
- GitHub Actions workflow configuration
- Defines schedule, triggers, and execution steps
- Installs Python dependencies and runs the monitoring script

### `ipo_monitor.py`
- Main Python script for IPO monitoring
- Fetches data from NASDAQ API
- Filters IPOs by date and offer amount
- Sends email notifications

## 🔒 Security Notes

- **Never commit secrets** to the repository
- Always use GitHub Secrets for sensitive data
- App Passwords are safer than regular Gmail passwords
- Repository can be private for additional security

## 📞 Support

If you encounter issues:

1. Check the **Actions** tab logs for error messages
2. Verify all secrets are correctly configured
3. Test the workflow manually before relying on scheduled runs
4. Review the troubleshooting section above

## ✅ Verification Checklist for Submission

Before submitting for review, ensure:

- [ ] Repository is created and files are uploaded
- [ ] All three secrets are configured (MAIL_PASS, EMAIL_FROM, EMAIL_TO)
- [ ] Workflow has been manually tested and runs successfully
- [ ] Email notification is received after test run
- [ ] Scheduled run is configured for 9:00 AM Dubai time
- [ ] Screen recording or repository access prepared for reviewer

## 🎯 What Reviewers Will See

When you provide repository access, reviewers can verify:

1. **Workflow Configuration**: Correct schedule and setup
2. **Execution Logs**: Successful runs with proper logging
3. **Code Quality**: Well-structured and commented Python code
4. **Error Handling**: Proper exception handling and notifications
5. **Automation**: Successful scheduled and manual executions

---

**Good luck with your submission! 🚀**
