import encodings.utf_8
import re
import random
from typing import Optional

from discord.ext import commands

TOKEN = "OTQxODI4OTA5MzI5MTU4MTc4.Ygbohg.tuUARD4LBblHC3EHr9Pmioa42-c"
GUILD = 'SWRPG Bot Dev'

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
    raise

def print_help(command=''):
    if command == 'roll':
        return f"Type the number of dice, and the letter afterwords to specify which dice you're rolling \n" \
               f"For example: !roll 1g1y2p will roll 1 green, 1 yellow, and 2 purple."


die_faces = {
    "G": [],
    "Y": 0,
    "B": 0,
    "P": 0,
    "R": 0,
    "BL": 0,
    "W": 0
}


def roll_dice(die):
    if die == 'B':
        return random.choice(['','','s','a','aa','as'])
    if die == 'G':
        return random.choice(['','s','s','a','a','as','aa','ss'])
    if die == 'Y':
        return random.choice(['','t','s','s','a','as','as','as','ss','ss','aa','aa'])
    if die == 'BL':
        return random.choice(['', '', 'f', 'f', 'd', 'd'])
    if die == 'P':
        return random.choice(['','f','d','d','d','ff','fd','dd'])
    if die == 'R':
        return random.choice(['','z','f','f','d','d','ff','ff','dd','dd','df','df'])

DICE_ROLL_REGEX = re.compile("(\d+bl)|(\d+BL)|(\d+[gG])|(\d+[yY])|(\d+[bB])|(\d+[pP])|(\d+[rR])|(\d+[wW])")

@bot.command(name="roll")
async def roll(ctx, dice_config: Optional[str] = '', roll_type: Optional[str] = ''):

    dice_config = dice_config.replace("C", "B").replace("c", "b")

    if dice_config.lower() == 'help' or dice_config.lower() == '':
        await ctx.send(print_help('roll'))
        await ctx.message.delete()
        return

    parsed_command = re.findall(DICE_ROLL_REGEX, dice_config)
    if parsed_command is None:
        await ctx.send(print_help('roll'))
        await ctx.message.delete()
        return

    current_dice = {"G": 0, "Y": 0, "B": 0, "P":0, "R": 0, "BL": 0, "W": 0}
    for match in parsed_command:
        record = [m for m in match if len(m) > 0][0]
        current_dice[re.sub(r"\d", r"", record.upper())] = int(re.sub( r"[a-zA-Z]", r"", record))

    response_string = ''
    dice_rolls_hist = []

    for key, value in current_dice.items():
        for _ in range(value):
            tmp_response = roll_dice(key)
            response_string += tmp_response
            dice_rolls_hist.append([key, tmp_response])

    advantages = response_string.count('a')
    disadvantages = response_string.count('d')
    successes = response_string.count('s')
    failures = response_string.count('f')
    triumphs = response_string.count('t')
    despairs = response_string.count('z')

    emoji_swaps = {
        "s": '\U0001f4a5',
        "f": '\U0001F53B',
        "a": '\U0001F531',
        "d": '\U0001F6D1',
        "t": '\U0001F387',
        "z": '\U0001F940'
    }

    for die_roll in dice_rolls_hist:
        for letter, emoji in emoji_swaps.items():
            die_roll[1] = die_roll[1].replace(letter, emoji)

    calculated_response = ''
    if successes >= failures:
        calculated_response += str('\U0001f4a5' * (successes - failures))
    else:
        calculated_response += '\U0001F53B' * (failures - successes)
    if advantages >= disadvantages:
        calculated_response += '\U0001F531' * (advantages - disadvantages)
    else:
        calculated_response += '\U0001F6D1'*(disadvantages - advantages)
    if triumphs >= despairs:
        calculated_response += '\U0001F387'*(triumphs - despairs)
    else:
        calculated_response += '\U0001F940'*(despairs - triumphs)


    response = (
        f"-------------------------------------------\n"
        + f"{ctx.author.name} "
        + (f"Roll: {roll_type} \n" if roll_type is not None or roll_type != '' else '\n')
        + f"Dice Roles: {dice_rolls_hist} \n"
        + f"Roll Outcome: {''.join(calculated_response)} \n"
        + f"-------------------------------------------"
    )

    await ctx.send(response)
    await ctx.message.delete()
    return


bot.run(TOKEN)