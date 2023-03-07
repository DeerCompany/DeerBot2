class CLEAR():
    def __init__(self):
        pass

    async def clear_all(self, ctx):
        await ctx.channel.purge(limit=None)

    async def clear(self, ctx, command):
        await ctx.channel.purge(limit=int(command))