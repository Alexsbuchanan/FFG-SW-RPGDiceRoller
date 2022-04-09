import time
from typing import List, Any, Union
import re
import discord
from discord import Interaction, InteractionResponse
from discord.ext.commands import Context

from models.Die import Die
from repositories.mongo.user_repository import get_or_add_user_from_context
from utils.dice_util import (
    get_dice_from_emoji_string,
    roll_dice,
    generate_dice_rolling_string,
    calculate_score,
    generate_score_string,
    generate_roll_string,
)


class DiceNumberEntry(discord.ui.TextInput):
    def __init__(self, num: int):
        super().__init__(
            label="Number of Dice",
            style=discord.TextStyle.short,
            placeholder="Num Dice",
            required=True,
            row=num,
        )

    # async def callback(self, interaction: Interaction) -> Any:
    #     view = self.view
    #     current_state: discord.ui.Select = view.children[0]
    #     die_to_fill = Die(current_state.values[0]).get_emoji_gif()
    #     content = interaction.message.content
    #     content = re.sub(die_to_fill, '', content)
    #
    #     await interaction.response.edit_message(
    #         content=content, view=view)


class DiceSubmitButton(discord.ui.Button):
    def __init__(self, num: int):
        super().__init__(
            style=discord.ButtonStyle.green, label="Roll!", row=num, disabled=False
        )

    async def callback(self, interaction: Interaction) -> Any:
        view = self.view
        await view.roll_dice(interaction.message.content)
        self.disabled = True
        await interaction.response.edit_message(view=view.clear_items())


class DiceIncrementButton(discord.ui.Button):
    def __init__(self, num: int):
        super().__init__(
            style=discord.ButtonStyle.green, emoji="➕", row=num, disabled=True
        )

    async def callback(self, interaction: Interaction) -> Any:
        view = self.view
        current_state: discord.ui.Select = view.children[0]
        selector_current_val = current_state.values[0]
        view.count += 1
        await interaction.response.edit_message(
            content=f"{interaction.message.content}{Die(current_state.values[0]).get_emoji_gif()}",
            view=view,
        )


class DiceDecrementButton(discord.ui.Button):
    def __init__(self, num: int):
        super().__init__(
            style=discord.ButtonStyle.red, emoji="➖", row=num, disabled=True
        )

    async def callback(self, interaction: Interaction) -> Any:
        view = self.view
        current_state: discord.ui.Select = view.children[0]
        view.count -= 1
        die_to_remove = Die(current_state.values[0]).get_emoji_gif()
        content = interaction.message.content
        content = re.sub(die_to_remove, "", content, 1)
        await interaction.response.edit_message(content=content, view=view)


class DiceSelectDropDownOption(discord.ui.Select):
    def __init__(self, num: int):
        drop_down_options = [
            discord.SelectOption(label=f"Ability", value="G", emoji=Die().GREEN_),
            discord.SelectOption(label="Boost", value="B", emoji=Die().BLUE_),
            discord.SelectOption(label="Setback", value="BL", emoji=Die().BLACK_),
            discord.SelectOption(label="Proficiency", value="Y", emoji=Die().YELLOW_),
            discord.SelectOption(label="Force", value="W", emoji=Die().GREEN_),
            discord.SelectOption(label="Challenge", value="R", emoji=Die().RED_),
            discord.SelectOption(label="Difficulty", value="P", emoji=Die().PURPLE_),
        ]

        super().__init__(options=drop_down_options, max_values=1, row=num)
        self.value = None
        self.num = num

    async def callback(self, interaction: Interaction) -> Any:
        assert self.view is not None

        view: DiceSelectDropDown = self.view
        state = view.children
        current_state = state[self.num]
        enabled_dice = current_state.values[0]
        new_die_type = Die(enabled_dice)
        for i in range(1, 3):
            state[i].disabled = False
        current_state.placeholder = new_die_type.get_die_name()
        await interaction.response.edit_message(view=view)


class DiceSelectDropDown(discord.ui.View):
    children: List[Union[DiceSelectDropDownOption, None]]

    def __init__(self, ctx: Context, timeout=None):
        super().__init__(timeout=timeout)

        self.count = 0
        self.ctx: Context = ctx
        (
            self.add_item(DiceSelectDropDownOption(0))
            .add_item(DiceDecrementButton(1))
            .add_item(DiceIncrementButton(1))
            .add_item(DiceSubmitButton(3))
            .add_item(DiceNumberEntry(4))
        )

    async def roll_dice(self, roll_value):
        user = get_or_add_user_from_context(self.ctx)
        dice = await get_dice_from_emoji_string(roll_value)
        await roll_dice(dice)
        roll_string = await generate_dice_rolling_string(dice)
        score = await calculate_score(dice)
        score_string, score_string_2 = await generate_score_string(score)
        if "rpname" in user.keys():
            tmp_response = f"Rolled By: {user['rpname']}\n"
        else:
            tmp_response = f"Rolled By: {user['author'].name}"
        tmp_response += roll_string + "\n"

        message = await self.ctx.send(roll_string)

        time.sleep(1)

        roll_string = await generate_roll_string(dice)
        await message.edit(content=roll_string)

        response = (
            f"Rolled By: "
            f"{user['rpname'] if 'rpname' in user.keys() and user['rpname'] is not None else self.ctx.author.name}\n"
        )
        response += f"Condensed: {score_string_2}"

        if len(response) > 2000:
            await self.ctx.send(
                "This dice roll too big yo. I'll figure it out soon doe. TY ❤️ <:Big_Chungus:949041751719550996>",
            )
        else:
            await self.ctx.send(response)


class EphemeralRoller(discord.ui.View):
    def __init__(self, user, ctx):
        super().__init__()
        self.user = user
        self.ctx = ctx
        self.username = self.user["rpname"] if "rpname" in self.user.keys() else ""

    @discord.ui.button(label=f"Choose your dice", style=discord.ButtonStyle.blurple)
    async def receive(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message(
            view=DiceSelectDropDown(self.ctx), ephemeral=True
        )
        await interaction.message.delete()
