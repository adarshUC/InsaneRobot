import re
import requests
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup




own_dict = eval(__import__("ast").literal_eval(requests.get('http://raw.githubusercontent.com/TeamScenario/DWords/main/words.txt').text).__str__())

@Client.on_message(filters.command("ud"))
async def udn(bot, m):
    text = m.text[len("/ud ") :]
    

    if len(m.text[len('/ud ') :])==0:
        text = 'ud'
    
    try:
        own_result = own_dict[text.upper()]
    except KeyError:
        pass
    else:
        return await m.reply_text(f'{text}\n\n{own_result}')

    results = requests.get(f"https://api.urbandictionary.com/v0/define?term={text}").json()
    btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Google it 🔍", url = f'https://google.com/search?q={re.sub("^.?ud.", "", text.replace(" ", "+"))}+meaning')
            ]
        ]
    )
    try:
        await m.reply(f'**{text}**\n\n{results["list"][0]["definition"].replace("[","").replace("]", "")}\n\n**Usage:**\n\n{results["list"][0]["example"].replace("[","").replace("]", "")}', reply_markup = btn)
    except Exception:
        await m.reply("No result found", reply_markup = btn)

__mod_name__ = "Dictionary"
__help__ = "/ud word - Get meaning of that word.\n\nExample: `/ud Hello`"
        
