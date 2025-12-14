import discord
from discord.ext import commands, tasks
import random
from datetime import datetime, time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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


def get_days_for_year(year):
    """Get the number of available days for a given year."""
    return DAYS_PER_YEAR.get(year, DEFAULT_DAYS)


def get_random_challenge():
    """Select a random year and day from Advent of Code."""
    year = random.randint(FIRST_YEAR, CURRENT_YEAR)
    max_day = get_days_for_year(year)
    day = random.randint(1, max_day)
    return year, day


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guild(s)')
    # Start the scheduled task
    friday_announcement.start()


@bot.command(name='spin')
async def spin_wheel(ctx):
    """Manually spin the wheel to get a random Advent of Code challenge."""
    year, day = get_random_challenge()
    await ctx.send(f"🎄 **Let's do Year {year} Day {day}!** 🎄\nhttps://adventofcode.com/{year}/day/{day}")


@bot.command(name='schedule')
async def show_schedule(ctx):
    """Show when the next Friday announcement will happen."""
    if friday_announcement.is_running():
        next_iteration = friday_announcement.next_iteration
        if next_iteration:
            await ctx.send(f"⏰ Next automatic announcement: {next_iteration.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        else:
            await ctx.send("⏰ Scheduler is running and will post on Fridays at 10:00 AM UTC")
    else:
        await ctx.send("⚠️ The Friday scheduler is not currently running.")


@tasks.loop(time=time(hour=0, minute=0)) # midnight UTC
async def friday_announcement():
    """Post a random Advent of Code challenge every Friday."""
    # Check if today is Friday (4)
    if datetime.now().weekday() == 4:
        year, day = get_random_challenge()
        
        # Send to all channels where the bot has permission
        for guild in bot.guilds:
            # Find a suitable channel (first text channel bot can send to)
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    await channel.send(
                        f"🎉 **Friday Advent of Code Challenge!** 🎉\n"
                        f"🎄 **Let's do Year {year} Day {day}!** 🎄\n"
                        f"https://adventofcode.com/{year}/day/{day}"
                    )
                    break  # Only send to one channel per server


@friday_announcement.before_loop
async def before_friday_announcement():
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
