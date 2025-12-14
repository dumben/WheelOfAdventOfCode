# WheelOfAdventOfCode Discord Bot

A Discord bot that randomly selects Advent of Code challenges and automatically posts them every Friday!

## Features

- 🎲 **Random Challenge Selection**: Picks a random year (2015-present) and day (1-25) from Advent of Code
- 📅 **Automatic Friday Posts**: Posts a new challenge every Friday at 12:00 AM UTC
- 🎮 **Manual Spin**: Use the `aoc!spin` command to get a challenge anytime
- ⏰ **Schedule Info**: Check when the next automatic post will happen with `aoc!schedule`

## Installation

### Quick Setup on Ubuntu

```bash
cd /opt
git clone https://github.com/dumben/WheelOfAdventOfCode.git adventbot
cd adventbot
```

For full deployment instructions including systemd service setup, see [deployment.md](deployment.md).

## Invite the Bot to Your Server

1. In the Developer Portal, go to "OAuth2" → "URL Generator"
2. Select these scopes:
   - `bot`
3. Select these bot permissions:
   - `Send Messages`
   - `Read Messages/View Channels`
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

## Commands

- `aoc!spin` - Manually get a random Advent of Code challenge
- `aoc!schedule` - See when the next automatic Friday announcement will happen

## License

MIT License - feel free to modify and use as you like!

## Contributing

Feel free to submit issues or pull requests to improve the bot!
