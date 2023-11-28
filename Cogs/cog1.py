from discord.ext import commands


class Cog1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="")
    async def command1(self, ctx):
        # some logic
        message = ""
        await ctx.send(message)


async def setup(bot):
    await bot.add_cog(Cog1(bot))
