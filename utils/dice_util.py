import re

from models.Die import Die


async def create_dice(ctx, dice_list):
    result_set = []
    for die in dice_list:
        number_of_dice_to_create = [int(num_dice) for num_dice in re.findall('\d+', die)][0]
        dice_color = re.findall('[a-zA-Z]', die)[0].upper()

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
            "despairs": 0
        }

    for die in dice:
        score_dict['successes'] += die.score_card['successes']
        score_dict['failures'] += die.score_card['failures']
        score_dict['advantages'] += die.score_card['advantages']
        score_dict['threats'] += die.score_card['threats']
        score_dict['triumphs'] += die.score_card['triumphs']
        score_dict['despairs'] += die.score_card['despairs']

    if score_dict['successes'] >= score_dict['failures']:
        score_dict['successes'] -= score_dict['failures']
        score_dict['failures'] = 0
    else:
        score_dict['failures'] -= score_dict['successes']
        score_dict['successes'] = 0

    if score_dict['advantages'] >= score_dict['threats']:
        score_dict['advantages'] -= score_dict['threats']
        score_dict['threats'] = 0
    else:
        score_dict['threats'] -= score_dict['advantages']
        score_dict['advantages'] = 0

    return score_dict

async def generate_score_string(score: dict):
    score_string: str = ""
    score_string += Die.SUCCESS * score['successes']
    score_string += Die.FAILURE * score['failures']
    score_string += Die.ADVANTAGE * score['advantages']
    score_string += Die.THREAT * score['threats']
    score_string += Die.TRIUMPH * score['triumphs']
    score_string += Die.DESPAIR * score['despairs']
    return score_string

async def generate_roll_string(dice):
    roll_string = 'Rolled:'
    for die in dice:
        roll_string += f"({die.die_emoji}-"
        if die.current_value is not None:
            roll_string += f"-{die.current_value}):"
        else:
            roll_string += f"-:"
    return roll_string