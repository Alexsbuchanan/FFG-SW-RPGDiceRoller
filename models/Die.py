import random
from typing import List, Union


class Die:


    _FFG_ABILITY = "FFG_Ability"
    _FFG_BOOST = "FFG_Boost"
    _FFG_CHALLENGE = "FFG_Challenge"
    _FFG_DIFFICULTY = "FFG_Difficulty"
    _FFG_PROFICIENCY = "FFG_Proficiency"
    _FFG_SETBACK = "FFG_Setback"

    _COLOR_ALIAS_ABILITY = "G"
    _COLOR_ALIAS_BOOST = "B"
    _COLOR_ALIAS_CHALLENGE = "R"
    _COLOR_ALIAS_DIFFICULTY = "P"
    _COLOR_ALIAS_PROFICIENCY = "Y"
    _COLOR_ALIAS_SETBACK = "BL"
    #Dice Face Emojis
    _SUCCESS = '<:success:949480296967991387>'
    _FAILURE = '<:failure:949480296976371772>'
    _ADVANTAGE = '<:advantage:949480296821166090>'
    _THREAT = '<:threat:949480297437757440>'
    _TRIUMPH = '<:triumph:949480297412571176>'
    _DESPAIR = '<:despair:949480296787628073>'
    # Dice Emojis
    _IMG_ABILITY_DIE = '<:abilitydie:949480296519180289>'
    _IMG_BOOST_DIE = '<:boostdie:949480296720523315>'
    _IMG_CHALLENGE_DIE = '<:challengedie:949480297504862218>'
    _IMG_DIFFICULTY_DIE = '<:difficultydie:949480296720527401>'
    _IMG_PROFICIENCY_DIE = '<:proficiencydie:949480297244790806>'
    _IMG_SETBACK_DIE = '<:setbackdie:949480297093816400>'

    _PURPLE_T = '<:purplet:949812877282410547>'
    _PURPLE_TT = '<:purplett:949812876984602644>'
    _PURPLE_ = '<:purple:949812874908422154>'
    _PURPLE_F = '<:purplef:949812876296728676>'
    _PURPLE_FF = '<:purpleff:949812876229636127>'
    _PURPLE_FT = '<:purpleft:949812876472885328>'
    _PURPLE_GIF = '<a:purplegif:949812877315932170>'

    def __init__(self, die_type = None, by_alias = True):
        if not by_alias and die_type is not None:
            self.type = die_type
        elif by_alias and die_type is not None:
            self.set_dice_type_by_color_alias(die_type)
        else:
            self.type = None

        self.die_emoji: str = ''
        self.get_emoji()
        self.die_faces: List  = []
        self.get_faces()
        self.num_faces: int = len(self.die_faces)
        self.current_value: Union[str, None] = None
        self.score_card = {
            "successes": 0,
            "failures": 0,
            "advantages": 0,
            "threats": 0,
            "triumphs": 0,
            "despairs": 0
        }

    def set_dice_type_by_color_alias(self, color_alias: str):
        if color_alias == self._COLOR_ALIAS_ABILITY:
            self.type = self._FFG_ABILITY
        elif color_alias == self._COLOR_ALIAS_BOOST:
            self.type = self._FFG_BOOST
        elif color_alias == self._COLOR_ALIAS_CHALLENGE:
            self.type = self._FFG_CHALLENGE
        elif color_alias == self._COLOR_ALIAS_SETBACK:
            self.type = self._FFG_SETBACK
        elif color_alias == self._COLOR_ALIAS_PROFICIENCY:
            self.type = self._FFG_PROFICIENCY
        elif color_alias == self._COLOR_ALIAS_DIFFICULTY:
            self.type = self._FFG_DIFFICULTY

    def get_emoji(self):
        emoji = None
        if self.type == self._FFG_ABILITY:
            emoji = self._IMG_ABILITY_DIE
        elif self.type == self._FFG_BOOST:
            emoji = self._IMG_BOOST_DIE
        elif self.type == self._FFG_CHALLENGE:
            emoji = self._IMG_CHALLENGE_DIE
        elif self.type == self._FFG_DIFFICULTY:
            emoji = self._IMG_DIFFICULTY_DIE
        elif self.type == self._FFG_PROFICIENCY:
            emoji = self._IMG_PROFICIENCY_DIE
        elif self.type == self._FFG_SETBACK:
            emoji = self._IMG_SETBACK_DIE
        self.die_emoji = emoji

    def get_faces(self):
        faces = []
        if self.type == self._FFG_BOOST:
            faces = [
                [None],
                [None],
                [self._SUCCESS],
                [self._ADVANTAGE],
                [self._ADVANTAGE, self._ADVANTAGE],
                [self._ADVANTAGE, self._SUCCESS]
            ]
        elif self.type == self._FFG_ABILITY:
            faces = [
                [None],
                [self._SUCCESS],
                [self._SUCCESS],
                [self._ADVANTAGE],
                [self._ADVANTAGE],
                [self._ADVANTAGE, self._SUCCESS],
                [self._ADVANTAGE, self._ADVANTAGE],
                [self._SUCCESS, self._SUCCESS]

            ]
        elif self.type == self._FFG_CHALLENGE:
            faces = [
                [None],
                [self._DESPAIR],
                [self._FAILURE],
                [self._FAILURE],
                [self._THREAT],
                [self._THREAT],
                [self._FAILURE, self._FAILURE],
                [self._FAILURE, self._FAILURE],
                [self._THREAT, self._THREAT],
                [self._THREAT, self._THREAT],
                [self._THREAT, self._FAILURE],
                [self._THREAT, self._FAILURE],
            ]
        elif self.type == self._FFG_DIFFICULTY:
            faces = [
                [None],
                [self._FAILURE],
                [self._THREAT],
                [self._THREAT],
                [self._THREAT],
                [self._FAILURE, self._FAILURE],
                [self._THREAT, self._FAILURE],
                [self._THREAT, self._THREAT],
            ]
        elif self.type == self._FFG_PROFICIENCY:
            faces = [
                [None],
                [self._TRIUMPH],
                [self._SUCCESS],
                [self._SUCCESS],
                [self._ADVANTAGE],
                [self._ADVANTAGE, self._SUCCESS],
                [self._ADVANTAGE, self._SUCCESS],
                [self._SUCCESS, self._SUCCESS],
                [self._SUCCESS, self._SUCCESS],
                [self._ADVANTAGE, self._ADVANTAGE],
                [self._ADVANTAGE, self._ADVANTAGE],
            ]
        elif self.type == self._FFG_SETBACK:
            faces = [
                [None],
                [None],
                [self._THREAT],
                [self._THREAT],
                [self._FAILURE],
                [self._FAILURE],
            ]

        self.die_faces = faces

    def get_type(self):
        return self.type

    def roll(self):
        self.current_value = random.choice(self.die_faces)
        for entry in self.current_value:
            if entry == self._SUCCESS:
                self.score_card['successes'] += 1
            elif entry == self._FAILURE:
                self.score_card['failures'] += 1
            elif entry == self._ADVANTAGE:
                self.score_card['advantages'] += 1
            elif entry == self._THREAT:
                self.score_card['threats'] += 1
            elif entry == self._TRIUMPH:
                self.score_card['triumphs'] += 1
            elif entry == self._DESPAIR:
                self.score_card['despairs'] += 1

    @property
    def DESPAIR(self):
        return self._DESPAIR

    @property
    def TRIUMPH(self):
        return self._TRIUMPH

    @property
    def THREAT(self):
        return self._THREAT

    @property
    def ADVANTAGE(self):
        return self._ADVANTAGE

    @property
    def FAILURE(self):
        return self._FAILURE

    @property
    def SUCCESS(self):
        return self._SUCCESS
