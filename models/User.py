import discord


class User:
    def __init__(self, member: discord.member.Member):
        self.id = member.id
        self.name = member.name
        self.display_name = member.display_name
        self.guild_name = member.guild.name
        self.guild_id = member.guild.id

    def convert_to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "guild_name": self.guild_name,
            "guild_id": self.guild_id,
        }
