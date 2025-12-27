# WheelOfAdventOfCode Discord Bot

A Discord bot that randomly selects Advent of Code challenges and automatically posts them every Friday!

## Features

- 🎲 **Random Challenge Selection**: Picks a random year (2015-present) and day (1-25) from Advent of Code
- 💻 **Suggested Language**: Randomly suggests a programming language (Python, Ruby, Java, Scala, or SQL) to add variety to your challenges
- 📅 **Customizable Schedule**: Each server can set its own announcement schedule (defaults to Fridays at 00:01 UTC)
- 🎮 **Manual Spin**: Use the `aoc!spin` command to get a challenge anytime
- ⏰ **Schedule Info**: Check when the next automatic post will happen with `aoc!schedule`

## Installation

For full deployment instructions including systemd service setup, see [deployment.md](deployment.md).

## Invite the Bot to Your Server

Use the [WheelOfAdventOfCode](https://discord.com/oauth2/authorize?client_id=1449599807613173881&permissions=68608&integration_type=0&scope=bot) bot invitation link, select your server and authorize the bot

## Commands

- `aoc!spin` - Manually get a random Advent of Code challenge
- `aoc!schedule` - See when the next automatic announcement will happen for your server
- `aoc!setschedule <day> <hour>` - (Admin only) Set the announcement schedule for your server
  - Example: `aoc!setschedule friday 18` (Every Friday at 6:00 PM UTC)
  - Day: monday, tuesday, wednesday, thursday, friday, saturday, sunday
  - Hour: 0-23 (UTC timezone)
  - Posts will be made at 1 minute past the specified hour

## License

MIT License - feel free to modify and use as you like!

## Contributing

Feel free to submit issues or pull requests to improve the bot!
