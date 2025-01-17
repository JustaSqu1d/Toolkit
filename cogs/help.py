import discord
from discord.utils import utcnow

from core import Cog, Context


class HelpSelect(discord.ui.Select):
    def __init__(self, cog: Cog) -> None:
        super().__init__(
            placeholder="Choose a category",
            options=[
                discord.SelectOption(
                    label=cog_name,
                    description=cog.__doc__,
                )
                for cog_name, cog in cog.bot.cogs.items()
                if cog.__cog_commands__
                and cog_name not in ["Jishaku", "Pycord", "Owner", "Help"]
            ],
        )
        self.cog = cog

    async def callback(self, interaction: discord.Interaction):
        cog_name = self.values[0]
        assert isinstance(cog_name, str)
        cog = self.cog.bot.get_cog(cog_name)
        assert cog
        embed = discord.Embed(
            title=f"{cog_name} Commands",
            description="\n".join(
                f"`/{command.qualified_name}`: {command.description}"  # type: ignore # description exists
                for command in cog.walk_commands()
            ),
            color=0x0060FF,
            timestamp=utcnow(),
        )
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )


class Help(Cog):
    @discord.slash_command(name="help")
    async def help_command(self, ctx: Context):
        """Get help about the bot, a command or a command category."""
        assert self.bot.user
        embed = discord.Embed(
            title=self.bot.user.name,
            description=(
                "A bot built to help you manage your Discord server as easily as possible.\n"
                "Use the menu below to view commands."
            ),
            colour=0x0060FF,
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(name="Server Count", value=str(len(self.bot.guilds)))
        embed.add_field(
            name="Member Count",
            value=str(sum(guild.member_count for guild in self.bot.guilds)),
        )
        embed.add_field(name="Ping", value=f"{self.bot.latency*1000:.2f}ms")

        await ctx.respond(embed=embed, view=discord.ui.View(HelpSelect(self)))


def setup(bot):
    bot.add_cog(Help(bot))
