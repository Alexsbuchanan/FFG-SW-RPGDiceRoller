import re
from discord.ext.commands.context import Context


def print_help(command=''):
   if command == 'roll':
      return f"Type the number of dice, and the letter afterwords to specify which dice you're rolling \n" \
             f"For example: !roll 1g1y2p will roll 1 green, 1 yellow, and 2 purple."


async def parse_roll(ctx: Context, input_string: str):
   """
   Parses the users input into a translated die roll
   :param ctx:
   :param input_string:
   :return:
   """
   standard_dice_roll_regex = re.compile("(\d+d\d+)")
   ffg_dice_roll_regex = re.compile("(\d+bl)|(\d+BL)|(\d+[gG])|(\d+[yY])|(\d+[bB])|(\d+[pP])|(\d+[rR])|(\d+[wW])")
   # Allow referring to "Blue" dice as "Cyan" with a c
   dice_config = input_string.replace("C", "B").replace("c", "b")

   if dice_config.lower() == 'help' or dice_config.lower() == '':
      await ctx.send(print_help('roll'))
      await ctx.message.delete()
      return

   parsed_command = re.findall(ffg_dice_roll_regex, dice_config)

   cleaned_result = []
   for command in parsed_command:
      for match in command:
         if len(match) > 0:
            cleaned_result.append(match)

   return cleaned_result
