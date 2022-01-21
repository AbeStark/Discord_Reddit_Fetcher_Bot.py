# Discord bot, searches subreddits for posts.

from discord.ext import commands
import logging
import asyncpraw
import secrets

# Logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Reddit api authorization.
reddit = asyncpraw.Reddit(
    client_id=secrets.client_id,
    client_secret=secrets.client_secret,
    user_agent=secrets.user_agent,
)

bot = commands.Bot(command_prefix="!")


@bot.event  # Bot active status notification.
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event  # Catches no command error.
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found")


@bot.command()  # Searches reddit based on user input.
async def subreddit(ctx, sub_name, sub_sort="hot", sub_limit=1):
    valid_sorts = ["hot", "confidence", "top", "new", "controversial", "old", "random", "qa", "live"]

    if sub_sort not in valid_sorts:
        await ctx.send("Invalid sort!: hot, confidence, top, new, controversial, old, random, qa, live.")

    if sub_sort == "hot":
        sub_request = await reddit.subreddit(sub_name)
        async for submission in sub_request.hot(limit=int(sub_limit)):
            await ctx.send(submission.title + submission.url)

    if sub_sort == "top":
        sub_request = await reddit.subreddit(sub_name)
        async for submission in sub_request.top(limit=int(sub_limit)):
            await ctx.send(submission.title + submission.url)

    if sub_sort == "new":
        sub_request = await reddit.subreddit(sub_name)
        async for submission in sub_request.new(limit=int(sub_limit)):
            await ctx.send(submission.title + submission.url)

    if sub_sort == "random":
        sub_request = await reddit.subreddit(sub_name)
        async for submission in sub_request.random(limit=int(sub_limit)):
            await ctx.send(submission.title + submission.url)


@subreddit.error  # Catches expected errors in the subreddit() command
async def subreddit_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Subreddit name is required.")

    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Subreddit Does not exist.")

    if isinstance(error, commands.BadArgument):
        await ctx.send("Post limit must be an integer.")


bot.run(secrets.token)
