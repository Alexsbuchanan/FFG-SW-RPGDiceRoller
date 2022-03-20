import time
from typing import Optional

import asyncio
from discord.ext import commands
from discord.ext.commands.context import Context

from repositories.mongo.user_repository import get_or_add_user_from_context, update_user
from utils import command_parser_util, dice_util

TOKEN = "OTQxODI4OTA5MzI5MTU4MTc4.Ygbohg.tuUARD4LBblHC3EHr9Pmioa42-c"

bot = commands.Bot(command_prefix="!")


def print_help(command=""):
    if command == "roll":
        return (
            f"Type the number of dice, and the letter afterwords to specify which dice you're rolling \n"
            f"For example: !roll 1g1y2p will roll 1 green, 1 yellow, and 2 purple."
        )


@bot.command(name="set-config")
async def set_config(ctx: Context, setting: str = "", *args) -> None:
    value = ' '.join(args)
    user = get_or_add_user_from_context(ctx)
    if setting not in ['rpname']:
        await ctx.message.delete()
        await ctx.author.send(f"{setting} is not a valid setting, only rpname "
                              f"is for now. You stinkin' womp rat! ❤️ <:Big_Chungus:949041751719550996>")
        return
    user[setting] = value
    user = update_user(user)
    await ctx.message.delete()
    await ctx.author.send(f"User setting updated. Set {setting} = {user[setting]}")


@bot.command(name="roll")
async def roll(
        ctx: Context, dice_config: Optional[str] = "", roll_tag: Optional[str] = None
) -> None:
    user = get_or_add_user_from_context(ctx)
    parsed_command = await command_parser_util.parse_roll(ctx, dice_config)
    # Don't do anything else if parsed commands didn't do anything useful.
    if parsed_command is None and dice_config != "help":
        await ctx.send(
            f"Uh oh! The command '!roll {dice_config}' could not be parsed to a roll"
        )
        return
    dice = await dice_util.create_dice(parsed_command)
    await dice_util.roll_dice(dice)
    roll_string = await dice_util.generate_dice_rolling_string(dice)
    score = await dice_util.calculate_score(dice)
    score_string, score_string_2 = await dice_util.generate_score_string(score)
    tmp_response = f"Rolled By: {user['rpname'] if user['rpname'] is not None else ctx.author.name}\n"
    if roll_tag is not None:
        tmp_response += f"Rolled for: {roll_tag}\n"
    tmp_response += roll_string + "\n"

    message = await ctx.send(roll_string, reference=ctx.message)

    time.sleep(1)

    roll_string = await dice_util.generate_roll_string(dice)
    await message.edit(content=roll_string)

    response = f"Rolled By: {user['rpname'] if 'rpname' in user.keys() and user['rpname'] is not None else ctx.author.name}\n"
    if roll_tag is not None:
        response += f"Rolled for: {roll_tag}\n"
    # response += roll_string + "\n"
    # response += f"Results: {score_string} \n"
    response += f"Condensed: {score_string_2}"

    if len(response) > 2000:
        await ctx.send(
            "This dice roll too big yo. I'll figure it out soon doe. TY ❤️ <:Big_Chungus:949041751719550996>",
            reference=ctx.message,
        )
    else:
        await ctx.send(response, reference=ctx.message)
    return


@bot.command(name="rollp")
async def roll_private(
        ctx: Context, dice_config: Optional[str] = "", roll_tag: Optional[str] = None
) -> None:
    await ctx.message.delete()
    user = get_or_add_user_from_context(ctx)
    parsed_command = await command_parser_util.parse_roll(ctx, dice_config)
    # Don't do anything else if parsed commands didn't do anything useful.
    if parsed_command is None and dice_config != "help":
        await ctx.author.send(
            f"Uh oh! The command '!roll {dice_config}' could not be parsed to a roll"
        )
        return
    dice = await dice_util.create_dice(parsed_command)
    await dice_util.roll_dice(dice)
    roll_string = await dice_util.generate_dice_rolling_string(dice)
    score = await dice_util.calculate_score(dice)
    score_string, score_string_2 = await dice_util.generate_score_string(score)
    tmp_response = f"Rolled By: {user['rpname'] if user['rpname'] is not None else ctx.author.name}\n"
    if roll_tag is not None:
        tmp_response += f"Rolled for: {roll_tag}\n"
    tmp_response += roll_string + "\n"

    roll_string = await dice_util.generate_roll_string(dice)
    await ctx.author.send(content=roll_string)

    response = f"Rolled By: {user['rpname'] if user['rpname'] is not None else ctx.author.name}\n"
    if roll_tag is not None:
        response += f"Rolled for: {roll_tag}\n"
    # response += roll_string + "\n"
    response += f"Results: {score_string} \n"
    response += f"Condensed: {score_string_2}"

    if len(response) > 2000:
        await ctx.author.send(
            "This dice roll too big yo. I'll figure it out soon doe. TY ❤️ <:Big_Chungus:949041751719550996>",
            reference=ctx.message,
        )
    else:
        await ctx.author.send(response)
    return


bot.run(TOKEN)
