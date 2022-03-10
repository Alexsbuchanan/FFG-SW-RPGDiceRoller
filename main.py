from typing import Optional

from discord.ext import commands
from discord.ext.commands.context import Context

from utils import command_parser_util, dice_util

TOKEN = "OTQxODI4OTA5MzI5MTU4MTc4.Ygbohg.tuUARD4LBblHC3EHr9Pmioa42-c"
GUILD = 'SWRPG Bot Dev'

bot = commands.Bot(command_prefix='!')


def print_help(command=''):
    if command == 'roll':
        return f"Type the number of dice, and the letter afterwords to specify which dice you're rolling \n" \
               f"For example: !roll 1g1y2p will roll 1 green, 1 yellow, and 2 purple."


@bot.command(name="roll")
async def roll(ctx: Context, dice_config: Optional[str] = '', roll_tag: Optional[str] = None):

    parsed_command = await command_parser_util.parse_roll(ctx, dice_config)

    await ctx.send('<a:purplegif:949812877315932170>')

    # Don't do anything else if parsed commands did do anything useful.
    if parsed_command is None:
        await ctx.send(f"Uh oh! The command '!roll {dice_config}' could not be parsed to a roll")
        return
    dice = await dice_util.create_dice(ctx, parsed_command)
    await dice_util.roll_dice(dice)

    roll_string = await dice_util.generate_roll_string(dice)
    role_hist_report = await ctx.send(roll_string, reference=ctx.message)

    score = await dice_util.calculate_score(dice)

    score_string = await dice_util.generate_score_string(score)

    response = f"Rolled By: {ctx.author.name}\n"
    if roll_tag is not None:
        response += f"Rolled for: {roll_tag}\n"
    response += f"Results: {score_string}"


    # Throws an error if the response is too long.
    if len(response) > 2000:
        await ctx.send("This dice roll too big yo. I'll figure it out soon doe. TY ❤️ <:Big_Chungus:949041751719550996>")
    else:
        await ctx.send(response, reference=ctx.message)
    return

bot.run(TOKEN)