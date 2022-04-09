import random
from typing import List, Union


class Die:
    # All configuyrations of the dice
    _FFG_ABILITY = "FFG_Ability"
    _FFG_BOOST = "FFG_Boost"
    _FFG_CHALLENGE = "FFG_Challenge"
    _FFG_DIFFICULTY = "FFG_Difficulty"
    _FFG_PROFICIENCY = "FFG_Proficiency"
    _FFG_SETBACK = "FFG_Setback"
    _FFG_FORCE = "FFG_Force"

    # Color alias constants
    _COLOR_ALIAS_ABILITY = "G"
    _COLOR_ALIAS_BOOST = "B"
    _COLOR_ALIAS_CHALLENGE = "R"
    _COLOR_ALIAS_DIFFICULTY = "P"
    _COLOR_ALIAS_PROFICIENCY = "Y"
    _COLOR_ALIAS_SETBACK = "BL"

    # Dice Face Emojis
    _SUCCESS = "<:success:949480296967991387>"
    _FAILURE = "<:failure:949480296976371772>"
    _ADVANTAGE = "<:advantage:949480296821166090>"
    _THREAT = "<:threat:949480297437757440>"
    _TRIUMPH = "<:triumph:949480297412571176>"
    _DESPAIR = "<:despair:949480296787628073>"

    # Dice Emojis
    _IMG_ABILITY_DIE = "<:abilitydie:949480296519180289>"
    _IMG_BOOST_DIE = "<:boostdie:949480296720523315>"
    _IMG_CHALLENGE_DIE = "<:challengedie:949480297504862218>"
    _IMG_DIFFICULTY_DIE = "<:difficultydie:949480296720527401>"
    _IMG_PROFICIENCY_DIE = "<:proficiencydie:949480297244790806>"
    _IMG_SETBACK_DIE = "<:setbackdie:949480297093816400>"

    _GREEN_GIF = "<a:greengif:949812877123018792>"
    _RED_GIF = "<a:redgif:949812876967809071>"
    _PURPLE_GIF = "<a:purplegif:949812877315932170>"
    _BLUE_GIF = "<a:bluegif:949812876808421407>"
    _YELLOW_GIF = "<a:yellowgif:949812877479542865>"
    _BLACK_GIF = "<a:blackgif:949812873478160425>"

    _PURPLE_T = "<:purplet:949812877282410547>"
    _PURPLE_TT = "<:purplett:949812876984602644>"
    _PURPLE_ = "<:purple:949812874908422154>"
    _PURPLE_F = "<:purplef:949812876296728676>"
    _PURPLE_FF = "<:purpleff:949812876229636127>"
    _PURPLE_FT = "<:purpleft:949812876472885328>"

    _GREEN_ = "<:green:949812874602229780>"
    _GREEN_A = "<:greena:949812875885699083>"
    _GREEN_S = "<:greens:949812876607107083>"
    _GREEN_AA = "<:greenaa:949812876921700393>"
    _GREEN_SA = "<:greensa:949812876976226364>"
    _GREEN_SS = "<:greenss:949812877102039070>"

    _BLUE_ = "<:blue:949812873201332244>"
    _BLUE_A = "<:bluea:949812875210403850>"
    _BLUE_S = "<:blues:949812875336253510>"
    _BLUE_AS = "<:bluesa:949812876338675802>"
    _BLUE_AA = "<:blueaa:949812876099584011>"

    _RED_ = "<:red:954825602144284782>"
    _RED_T = "<:redt:949812877060100096>"
    _RED_TT = "<:redtt:949812877047525376>"
    _RED_FT = "<:redft:949812877043322910>"
    _RED_D = "<:redd:949812877034926100>"
    _RED_F = "<:redf:949812876699381810>"
    _RED_FF = "<:redff:949812876649041960>"

    _YELLOW_ = "<:yellow:949812875147493436>"
    _YELLOW_AA = "<:yellowaa:949812876904906783>"
    _YELLOW_A = "<:yellowa:949812877110431744>"
    _YELLOW_R = "<:yellowr:949812877152366673>"
    _YELLOW_S = "<:yellows:949812877156560976>"
    _YELLOW_SS = "<:yellowss:949812877185937408>"
    _YELLOW_SA = "<:yellowsa:949812877274005574>"

    _BLACK_ = "<:black:949812873016786971>"
    _BLACK_F = "<:blackf:949812873004187759>"
    _BLACK_T = "<:blackt:949812874715463751>"

    def __init__(self, die_type: str = None, by_alias: bool = True):
        if die_type is not None:
            die_type = die_type.upper()
        if not by_alias and die_type is not None:
            self.type = die_type
        elif by_alias and die_type is not None:
            self.set_dice_type_by_color_alias(die_type)
        else:
            self.type = None

        self.die_gif: str = ""
        self.get_emoji_gif()
        self.die_faces: List = []
        self.get_faces()
        self.num_faces: int = len(self.die_faces)
        self.current_value: Union[str, None] = None
        self.score_card = {
            "successes": 0,
            "failures": 0,
            "advantages": 0,
            "threats": 0,
            "triumphs": 0,
            "despairs": 0,
        }

    def get_die_name(self):
        if self.type == self._FFG_ABILITY:
            return self._FFG_ABILITY[4:]
        elif self.type == self._FFG_BOOST:
            return self._FFG_BOOST[4:]
        elif self.type == self._FFG_SETBACK:
            return self._FFG_SETBACK[4:]
        elif self.type == self._FFG_CHALLENGE:
            return self._FFG_CHALLENGE[4:]
        elif self.type == self._FFG_DIFFICULTY:
            return self._FFG_DIFFICULTY[4:]
        elif self.type == self._FFG_FORCE:
            return self._FFG_FORCE[4:]
        elif self.type == self._FFG_PROFICIENCY:
            return self._FFG_PROFICIENCY[4:]

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

    def get_emoji_gif(self):
        emoji_gif = None
        if self.type == self._FFG_ABILITY:
            emoji_gif = self._GREEN_GIF
        elif self.type == self._FFG_BOOST:
            emoji_gif = self._BLUE_GIF
        elif self.type == self._FFG_CHALLENGE:
            emoji_gif = self._RED_GIF
        elif self.type == self._FFG_DIFFICULTY:
            emoji_gif = self._PURPLE_GIF
        elif self.type == self._FFG_PROFICIENCY:
            emoji_gif = self._YELLOW_GIF
        elif self.type == self._FFG_SETBACK:
            emoji_gif = self._BLACK_GIF
        self.die_gif = emoji_gif
        return self.die_gif

    def get_faces(self):
        faces = []
        if self.type == self._FFG_BOOST:
            faces = [
                [None],
                [None],
                [self._SUCCESS],
                [self._ADVANTAGE],
                [self._ADVANTAGE, self._ADVANTAGE],
                [self._ADVANTAGE, self._SUCCESS],
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
                [self._SUCCESS, self._SUCCESS],
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
        return self

    def get_corresponding_die_face(self):

        if self.type == self._FFG_BOOST:
            if self.current_value == [None]:
                return self._BLUE_
            if self.current_value == [self._SUCCESS]:
                return self._BLUE_S
            if self.current_value == [self._ADVANTAGE]:
                return self._BLUE_A
            if self.current_value == [self._ADVANTAGE, self._ADVANTAGE]:
                return self._BLUE_AA
            if self.current_value == [self._ADVANTAGE, self._SUCCESS]:
                return self._BLUE_AS
        elif self.type == self._FFG_ABILITY:
            if self.current_value == [None]:
                return self._GREEN_
            if self.current_value == [self._SUCCESS]:
                return self._GREEN_S
            if self.current_value == [self._ADVANTAGE]:
                return self._GREEN_A
            if self.current_value == [self._ADVANTAGE, self._SUCCESS]:
                return self._GREEN_SA
            if self.current_value == [self._ADVANTAGE, self._ADVANTAGE]:
                return self._GREEN_AA
            if self.current_value == [self._SUCCESS, self._SUCCESS]:
                return self._GREEN_SS
        elif self.type == self._FFG_CHALLENGE:
            if self.current_value == [None]:
                return self._RED_
            if self.current_value == [self._DESPAIR]:
                return self._RED_D
            if self.current_value == [self._FAILURE]:
                return self._RED_F
            if self.current_value == [self._THREAT]:
                return self._RED_T
            if self.current_value == [self._FAILURE, self._FAILURE]:
                return self._RED_FF
            if self.current_value == [self._THREAT, self._THREAT]:
                return self._RED_TT
            if self.current_value == [self._THREAT, self._FAILURE]:
                return self._RED_FT
        elif self.type == self._FFG_DIFFICULTY:
            if self.current_value == [None]:
                return self._PURPLE_
            if self.current_value == [self._FAILURE]:
                return self._PURPLE_F
            if self.current_value == [self._THREAT]:
                return self._PURPLE_T
            if self.current_value == [self._FAILURE, self._FAILURE]:
                return self._PURPLE_FF
            if self.current_value == [self._THREAT, self._FAILURE]:
                return self._PURPLE_FT
            if self.current_value == [self._THREAT, self._THREAT]:
                return self._PURPLE_TT
        elif self.type == self._FFG_PROFICIENCY:
            if self.current_value == [None]:
                return self._YELLOW_
            if self.current_value == [self._TRIUMPH]:
                return self._YELLOW_R
            if self.current_value == [self._SUCCESS]:
                return self._YELLOW_S
            if self.current_value == [self._ADVANTAGE]:
                return self._YELLOW_A
            if self.current_value == [self._ADVANTAGE, self._SUCCESS]:
                return self._YELLOW_SA
            if self.current_value == [self._SUCCESS, self._SUCCESS]:
                return self._YELLOW_SS
            if self.current_value == [self._ADVANTAGE, self._ADVANTAGE]:
                return self._YELLOW_AA
        elif self.type == self._FFG_SETBACK:
            if self.current_value == [None]:
                return self._BLACK_
            if self.current_value == [self._THREAT]:
                return self._BLACK_T
            if self.current_value == [self._FAILURE]:
                return self._BLACK_F
        return self

    def get_type(self):
        return self.type

    def roll(self):
        self.current_value = random.choice(self.die_faces)
        print(f"Die {self.type} Rolled a: {self.current_value}")
        for entry in self.current_value:
            if entry == self._SUCCESS:
                self.score_card["successes"] += 1
            elif entry == self._FAILURE:
                self.score_card["failures"] += 1
            elif entry == self._ADVANTAGE:
                self.score_card["advantages"] += 1
            elif entry == self._THREAT:
                self.score_card["threats"] += 1
            elif entry == self._TRIUMPH:
                self.score_card["triumphs"] += 1
            elif entry == self._DESPAIR:
                self.score_card["despairs"] += 1
        return self

    @property
    def GREEN_(self):
        return self._GREEN_

    @property
    def RED_(self):
        return self._RED_

    @property
    def PURPLE_(self):
        return self._PURPLE_

    @property
    def BLACK_(self):
        return self._BLACK_

    @property
    def YELLOW_(self):
        return self._YELLOW_

    @property
    def BLUE_(self):
        return self._BLUE_

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
