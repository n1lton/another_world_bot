import discord, traceback
from discord.ext import commands

async def on_application_command_error(ctx: discord.ApplicationContext, error: Exception):
    if isinstance(error, commands.MissingRole) or isinstance(error, commands.MissingAnyRole):
        await ctx.respond(
            '❌ Нет прав для использования этой команды',
            ephemeral=True
        )

    else:
        await ctx.respond(
            embed=discord.Embed(
                title='Произошла ошибка!',
                description=error.with_traceback(),
                color=0xFF0000
            ),
            ephemeral=True
        )
        raise error


def setup(bot):
    bot.event(on_application_command_error)