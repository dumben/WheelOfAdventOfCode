# Setup

## **Done** Create a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name (e.g., "WheelOfAdventOfCode")
3. Go to the "Bot" section in the left sidebar
4. Click "Add Bot"
5. Under "Privileged Gateway Intents", enable:
   - **Message Content Intent** (required for commands)
6. Click "Reset Token" and copy your bot token

## Digital Ocean Ubuntu Droplet

### 1. Deploy to Digital Ocean Droplet

SSH into your droplet and clone the repository:
```bash
ssh root@your-droplet-ip
cd /opt
git clone https://github.com/dumben/WheelOfAdventOfCode.git adventbot
cd adventbot
```

### 2. Install Dependencies

On the droplet:
```bash
cd /opt/adventbot
apt update
apt install -y python3 python3-pip python3-venv

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies in venv
pip install -r requirements.txt

# Deactivate venv (we'll use the full path in systemd)
deactivate
```

### 3. Configure the Bot Token

Create a `.env` file to store your Discord bot token securely:
```bash
vi /opt/adventbot/.env
```

Add your token (replace with your actual token from step 1):
```
DISCORD_BOT_TOKEN=your-actual-token-here
```

Save and exit.

Secure the file so only root can read it:
```bash
chmod 600 /opt/adventbot/.env
chown root:root /opt/adventbot/.env
```

### 4. Create Systemd Service

Create the service file:
```bash
vi /etc/systemd/system/adventbot.service
```

Add this configuration:
```ini
[Unit]
Description=WheelOfAdventOfCode Discord Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/adventbot
EnvironmentFile=/opt/adventbot/.env
ExecStart=/opt/adventbot/venv/bin/python wheel_of_advent_of_code.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Save and exit.

### 5. Enable and Start the Service

```bash
# Reload systemd to recognize the new service
systemctl daemon-reload

# Enable the service to start on boot
systemctl enable adventbot

# Start the service now
systemctl start adventbot
```

### 6. Verify the Bot is Running

```bash
# Check service status
systemctl status adventbot

# View live logs
journalctl -u adventbot -f

# View recent logs
journalctl -u adventbot -n 50
```

You should see a message like "WheelOfAdventOfCode#1234 has connected to Discord!" in the logs.


## Managing the Service

```bash
# Stop the bot
systemctl stop adventbot

# Restart the bot (after making changes)
systemctl restart adventbot

# Check service status
systemctl status adventbot

# View live logs
journalctl -u adventbot -f

# Disable auto-start on boot (if needed)
systemctl disable adventbot
```

## Updating the Bot

When updates are pushed to the repository:

```bash
# SSH into your droplet
ssh root@your-droplet-ip

# Navigate to the bot directory
cd /opt/adventbot

# Pull the latest changes
git pull origin main

# If requirements.txt changed, update dependencies
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Restart the service
systemctl restart adventbot

# Check it's running
systemctl status adventbot
```

Or as a one-liner from your local machine:
```bash
ssh root@your-droplet-ip "cd /opt/adventbot && git pull origin main && systemctl restart adventbot"
```

## Troubleshooting

**Bot doesn't respond to commands:**
- Make sure "Message Content Intent" is enabled in the Discord Developer Portal
- Verify the bot has "Send Messages" permission in the channel

**Friday posts aren't working:**
- The bot must be running continuously
- Check the timezone - the schedule is in UTC
- Use `aoc!schedule` to verify the task is running

**Bot can't find the token:**
- Ensure the environment variable is set correctly
- Check for typos in the variable name
- Try printing `os.getenv('DISCORD_BOT_TOKEN')` to debug