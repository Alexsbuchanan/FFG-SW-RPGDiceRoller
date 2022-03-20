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
    }

    for die in dice:
        score_dict["successes"] += die.score_card["successes"]
        score_dict["failures"] += die.score_card["failures"]
        score_dict["advantages"] += die.score_card["advantages"]
        score_dict["threats"] += die.score_card["threats"]
        score_dict["triumphs"] += die.score_card["triumphs"]
        score_dict["despairs"] += die.score_card["despairs"]

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

    score_string_2: str = ""
    if score['successes'] > 0:
        score_string_2 += f"{score['successes']}{str(Die().SUCCESS)} • "
    if score['failures'] > 0:
        score_string_2 += f"{score['failures']}{str(Die().FAILURE)} • "
    if score['advantages'] > 0:
        score_string_2 += f"{score['advantages']}{str(Die().ADVANTAGE)} • "
    if score['threats'] > 0:
        score_string_2 += f"{score['threats']}{str(Die().THREAT)} • "
    if score['triumphs'] > 0:
        score_string_2 += f"{score['triumphs']}{str(Die().TRIUMPH)} • "
    if score['despairs'] > 0:
        score_string_2 += f"{score['despairs']}{str(Die().DESPAIR)}"

    score_string_2 = score_string_2.rsplit("• ", maxsplit=1)[0]

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
