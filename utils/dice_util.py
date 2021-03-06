import re

from models.Die import Die


async def create_dice(dice_list):
    result_set = []
    for die in dice_list:
        number_of_dice_to_create = [
            int(num_dice) for num_dice in re.findall("\d+", die)
        ][0]
        dice_color = "".join(re.findall("[a-zA-Z]", die)).upper()

        result_set += [Die(dice_color) for _ in range(number_of_dice_to_create)]

    return result_set


async def roll_dice(dice):
    for die in dice:
        die.roll()


async def calculate_score(dice):
    score_dict = {
        "successes": 0,
        "failures": 0,
        "advantages": 0,
        "threats": 0,
        "triumphs": 0,
        "despairs": 0,
        "light_sides": 0,
        "dark_sides": 0,
    }

    for die in dice:
        score_dict["successes"] += die.score_card["successes"]
        score_dict["failures"] += die.score_card["failures"]
        score_dict["advantages"] += die.score_card["advantages"]
        score_dict["threats"] += die.score_card["threats"]
        score_dict["triumphs"] += die.score_card["triumphs"]
        score_dict["despairs"] += die.score_card["despairs"]
        score_dict["light_sides"] += die.score_card["light_sides"]
        score_dict["dark_sides"] += die.score_card["dark_sides"]

    if score_dict["successes"] >= score_dict["failures"]:
        score_dict["successes"] -= score_dict["failures"]
        score_dict["failures"] = 0
    else:
        score_dict["failures"] -= score_dict["successes"]
        score_dict["successes"] = 0

    if score_dict["advantages"] >= score_dict["threats"]:
        score_dict["advantages"] -= score_dict["threats"]
        score_dict["threats"] = 0
    else:
        score_dict["threats"] -= score_dict["advantages"]
        score_dict["advantages"] = 0

    return score_dict


async def generate_score_string(score: dict):
    score_string: str = ""
    score_string += str(Die().SUCCESS) * score["successes"]
    score_string += str(Die().FAILURE) * score["failures"]
    score_string += str(Die().ADVANTAGE) * score["advantages"]
    score_string += str(Die().THREAT) * score["threats"]
    score_string += str(Die().TRIUMPH) * score["triumphs"]
    score_string += str(Die().DESPAIR) * score["despairs"]
    score_string += str(Die().LIGHTSIDE) * score["light_sides"]
    score_string += str(Die().DARKSIDE) * score["dark_sides"]

    score_string_2: str = ""
    if score["successes"] > 0:
        score_string_2 += f"{score['successes']}{str(Die().SUCCESS)} ??? "
    if score["failures"] > 0:
        score_string_2 += f"{score['failures']}{str(Die().FAILURE)} ??? "
    if score["advantages"] > 0:
        score_string_2 += f"{score['advantages']}{str(Die().ADVANTAGE)} ??? "
    if score["threats"] > 0:
        score_string_2 += f"{score['threats']}{str(Die().THREAT)} ??? "
    if score["triumphs"] > 0:
        score_string_2 += f"{score['triumphs']}{str(Die().TRIUMPH)} ??? "
    if score["despairs"] > 0:
        score_string_2 += f"{score['despairs']}{str(Die().DESPAIR)} ??? "
    if score["light_sides"] > 0:
        score_string_2 += f"{score['light_sides']}{str(Die().LIGHTSIDE)} ??? "
    if score["dark_sides"] > 0:
        score_string_2 += f"{score['dark_sides']}{str(Die().DARKSIDE)} ??? "

    score_string_2 = score_string_2.rsplit("??? ", maxsplit=1)[0]

    return score_string, score_string_2


async def generate_dice_rolling_string(dice):
    roll_string = ""
    for die in dice:
        roll_string += die.die_gif
    return roll_string


async def generate_roll_string(dice):
    roll_string = ""
    for die in dice:
        roll_string += die.get_corresponding_die_face()
    return roll_string


async def get_dice_from_emoji_string(emoji_string):
    green = Die()._GREEN_GIF
    red = Die()._RED_GIF
    yellow = Die()._YELLOW_GIF
    black = Die()._BLACK_GIF
    blue = Die()._BLUE_GIF
    purple = Die()._PURPLE_GIF
    white = Die()._WHITE_GIF

    _, num_green = re.subn(green, "", emoji_string)
    _, num_red = re.subn(red, "", emoji_string)
    _, num_yellow = re.subn(yellow, "", emoji_string)
    _, num_black = re.subn(black, "", emoji_string)
    _, num_blue = re.subn(blue, "", emoji_string)
    _, num_purple = re.subn(purple, "", emoji_string)
    _, num_white = re.subn(white, "", emoji_string)

    roll_string = (
        [f"G{num_green}"]
        + [f"R{num_red}"]
        + [f"Y{num_yellow}"]
        + [f"BL{num_black}"]
        + [f"B{num_blue}"]
        + [f"P{num_purple}"]
        + [f"W{num_white}"]
    )
    dice = await create_dice(roll_string)
    return dice
