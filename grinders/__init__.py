from .gridners import Grinders


async def setup(bot):
    await bot.add_cog(Grinders(bot))
