import discord, config
from discord.ext import commands
from autocomplete import get_groups
from database import db
from models.Group import Group
from bot import bot


class InputMessage(discord.ui.Modal):
    def __init__(self, group, *args, **kwargs):
        super().__init__(*args, title='Рассылка', **kwargs)
        self.group = group
        self.add_item(
            discord.ui.InputText(
                style=discord.InputTextStyle.paragraph,
                label='Сообщение',
                placeholder='Привет, мир!',
                max_length=2000
            )
        )

    
    async def callback(self, interaction: discord.Interaction):
        await interaction.respond('✅ Сообщение отправлено', ephemeral=True)
        for channel in self.group.channels:
            discord_channel = bot.get_channel(channel.id)
            await discord_channel.send(self.children[0].value)


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@commands.slash_command(name='отправить-сообщение', description='Отправить уведомление в группу')
@discord.commands.option('название-группы', str, required=True,
        parameter_name='group_name', autocomplete=get_groups,
        description='Выберите группу для рассылки')
async def send_message(ctx: discord.ApplicationContext, group_name: str):
    group = db.query(Group).filter(Group.name == group_name).first()
    if not group:
        await ctx.respond('❌ Группа не найдена', ephemeral=True)
        return
    
    await ctx.send_modal(InputMessage(group))


def setup(group: discord.SlashCommandGroup):
    send_message.parent = group
    group.add_command(send_message)