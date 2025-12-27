import discord
from discord.ext import commands, tasks
import random
from datetime import datetime, time, timedelta
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Server settings file
SETTINGS_FILE = 'server_settings.json'

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='aoc!', intents=intents)

# Advent of Code runs from 2015 to current year
FIRST_YEAR = 2015
CURRENT_YEAR = datetime.now().year

# Default number of days for years not specified
DEFAULT_DAYS = 25

# Days available per year
DAYS_PER_YEAR = {
    2025: 12,
}

# Suggested languages with weights
CHALLENGE_LANGUAGE = {
    "Python": 1.0,
    "Ruby": 1.0,
    "Java": 0.2,
    "Scala": 0.1,
    "SQL": 0.1
}

# Default schedule settings
DEFAULT_SCHEDULE = {
    "day": 4,  # Friday (0=Monday, 6=Sunday)
    "hour": 0
}


def load_server_settings():
    """Load server settings from JSON file."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def save_server_settings(settings):
    """Save server settings to JSON file."""
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)


def get_server_schedule(guild_id):
    """Get schedule settings for a specific server."""
    settings = load_server_settings()
    server_id = str(guild_id)
    if server_id in settings and 'schedule' in settings[server_id]:
        return settings[server_id]['schedule']
    return DEFAULT_SCHEDULE.copy()



def get_days_for_year(year):
    """Get the number of available days for a given year."""
    return DAYS_PER_YEAR.get(year, DEFAULT_DAYS)


def get_random_challenge():
    """Select a random year and day from Advent of Code."""
    year = random.randint(FIRST_YEAR, CURRENT_YEAR)
    max_day = get_days_for_year(year)
    day = random.randint(1, max_day)
    return year, day


def get_random_language():
    """Select a random language based on weights."""
    languages = list(CHALLENGE_LANGUAGE.keys())
    weights = list(CHALLENGE_LANGUAGE.values())
    return random.choices(languages, weights=weights, k=1)[0]


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guild(s)')
    # Start the scheduled task
    weekly_announcement.start()


@bot.command(name='spin')
async def spin_wheel(ctx):
    """Manually spin the wheel to get a random Advent of Code challenge."""
    year, day = get_random_challenge()
    language = get_random_language()
    await ctx.send(
        f"🎄 **Let's do Year {year} Day {day}!** 🎄\n"
        f"💻 **Suggested Language: {language}** 💻\n"
        f"https://adventofcode.com/{year}/day/{day}"
    )


@bot.command(name='schedule')
async def show_schedule(ctx):
    """Show when the next announcement will happen for this server."""
    if weekly_announcement.is_running():
        schedule = get_server_schedule(ctx.guild.id)
        target_day = schedule['day']
        target_hour = schedule['hour']

        # Day names
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Calculate next occurrence (at 1 minute past the hour)
        now = datetime.now()
        days_until_target = (target_day - now.weekday()) % 7
        if days_until_target == 0 and (now.hour > target_hour or (now.hour == target_hour and now.minute >= 1)):
            # If it's today but already past the time, get next week
            days_until_target = 7
        next_post = now.replace(hour=target_hour, minute=1, second=0, microsecond=0)
        next_post = next_post + timedelta(days=days_until_target)

        await ctx.send(
            f"⏰ Next automatic announcement: {next_post.strftime('%Y-%m-%d %H:%M:%S')} UTC ({day_names[target_day]})\n"
            f"📅 Current schedule: Every {day_names[target_day]} at {target_hour:02d}:00 UTC"
        )
    else:
        await ctx.send("⚠️ The scheduler is not currently running.")


@bot.command(name='setschedule')
@commands.has_permissions(administrator=True)
async def set_schedule(ctx, day: str, hour: int):
    """Set the announcement schedule for this server (admin only).

    Usage: aoc!setschedule <day> <hour>
    Day: monday, tuesday, wednesday, thursday, friday, saturday, sunday
    Hour: 0-23 (UTC)

    Example: aoc!setschedule friday 18
    """
    # Parse day
    day_map = {
        'monday': 0, 'mon': 0,
        'tuesday': 1, 'tue': 1, 'tues': 1,
        'wednesday': 2, 'wed': 2, 'weds': 2,
        'thursday': 3, 'thu': 3, 'thur': 3, 'thurs': 3,
        'friday': 4, 'fri': 4,
        'saturday': 5, 'sat': 5,
        'sunday': 6, 'sun': 6
    }

    day_lower = day.lower()
    if day_lower not in day_map:
        await ctx.send("❌ Invalid day. Use: monday, tuesday, wednesday, thursday, friday, saturday, or sunday")
        return

    day_num = day_map[day_lower]

    # Validate hour
    if not (0 <= hour <= 23):
        await ctx.send("❌ Hour must be between 0 and 23 (UTC)")
        return

    # Save settings
    settings = load_server_settings()
    server_id = str(ctx.guild.id)

    if server_id not in settings:
        settings[server_id] = {}

    settings[server_id]['schedule'] = {
        'day': day_num,
        'hour': hour
    }

    save_server_settings(settings)

    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    await ctx.send(
        f"✅ Schedule updated!\n"
        f"📅 New schedule: Every {day_names[day_num]} at {hour:02d}:00 UTC"
    )


@set_schedule.error
async def set_schedule_error(ctx, error):
    """Handle errors for the setschedule command."""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need administrator permissions to change the schedule.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "❌ Missing required argument.\n"
            "Usage: `aoc!setschedule <day> <hour>`\n"
            "Example: `aoc!setschedule friday 18`"
        )
    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "❌ Invalid argument format.\n"
            "Hour must be a number (0-23).\n"
            "Example: `aoc!setschedule friday 18`"
        )


@tasks.loop(hours=1)  # Check every hour
async def weekly_announcement():
    """Post a random Advent of Code challenge based on each server's schedule."""
    now = datetime.now()

    current_day = now.weekday()
    current_hour = now.hour

    # Check each server's schedule
    for guild in bot.guilds:
        schedule = get_server_schedule(guild.id)

        # Check if it's time to post for this server
        if schedule['day'] == current_day and schedule['hour'] == current_hour:
            year, day = get_random_challenge()
            language = get_random_language()

            # Find a suitable channel (first text channel bot can send to)
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    await channel.send(
                        f"🎉 **Scheduled Advent of Code Challenge!** 🎉\n"
                        f"🎄 **Let's do Year {year} Day {day}!** 🎄\n"
                        f"💻 **Suggested Language: {language}** 💻\n"
                        f"https://adventofcode.com/{year}/day/{day}"
                    )
                    break  # Only send to one channel per server


@weekly_announcement.before_loop
async def weekly_announcement():
    """Wait until the bot is ready before starting the loop."""
    await bot.wait_until_ready()


# Run the bot
if __name__ == '__main__':
    # Get token from environment variable
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    
    if not TOKEN:
        print("Error: DISCORD_BOT_TOKEN environment variable not set!")
        print("Please set it with your bot token:")
        print("  export DISCORD_BOT_TOKEN='your-token-here'")
    else:
        bot.run(TOKEN)
