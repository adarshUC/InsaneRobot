
━━━━━━━━━━━━━━━━━━━━

<h2>  ᴅᴇᴘʟᴏʏ ᴏɴ ʜᴇʀᴏᴋᴜ​ 🚀</h2> 
ᴛʜᴇ ᴇᴀsɪᴇsᴛ ᴡᴀʏ ᴛᴏ ᴅᴇᴘʟᴏʏ  ɢʀᴏᴜᴘ ᴄᴏɴᴛʀᴏʟʟᴇʀ 
<p align="center"><a href="https://heroku.com/deploy?template=https://github.com/adarshuc/InsaneRobot"> <img src="https://img.shields.io/badge/Deploy%20To%20Heroku-black?style=for-the-badge&logo=heroku" width="220" height="38.45"/></a></p>
━━━━━━━━━━━━━━━━━━━━
<h3 align="center">
    ─「 ᴅᴇᴩʟᴏʏ ᴏɴ ᴠᴘs/ʟᴏᴄᴀʟ 」─
</h3>


<h3>
- <b> ᴠᴘs/ʟᴏᴄᴀʟ ᴅᴇᴘʟᴏʏᴍᴇɴᴛ ᴍᴇᴛʜᴏᴅ </b>
</h3>

- Get your [Necessary Variables](https://github.com/adarshuc/InsaneRobot/blob/main/InsaneRobot/config.py)
- Upgrade and Update by :
`sudo apt-get update && sudo apt-get upgrade -y`
- Install required packages by :
`sudo apt-get install python3-pip -y`
- Install pip by :
`sudo pip3 install -U pip`
- Clone the repository by :
`git clone https://github.com/adarshuc/InsaneRobot && cd InsaneRobot`
- Install/Upgrade setuptools by :
`pip3 install --upgrade pip setuptools`
- Install requirements by :
`pip3 install -U -r requirements.txt`
- Fill your variables in config by :
`vi InsaneRobot/config.py`

Press `I` on the keyboard for editing config

Press `Ctrl+C` when you're done with editing config and `:wq` to save the config
- Install tmux to keep running your bot when you close the terminal by :
`sudo apt install tmux && tmux`
- Finally run the bot by :
`python3 -m InsaneRobot`
- For getting out from tmux session

Press `Ctrl+b` and then `d`

<p align="center">
  <img src="https://te.legra.ph/file/5ab0e91166940c796f7dc.jpg">
</p>


━━━━━━━━━━━━━━━━━━━━


<h2 align="center"> 
    ᴡʀɪᴛᴇ ɴᴇᴡ ᴍᴏᴅᴜʟᴇs 
</h2>

```py
#ᴀᴅᴅ ʟɪᴄᴇɴsᴇ ᴛᴇxᴛ ʜᴇʀᴇ ɢᴇᴛ ɪᴛ ғʀᴏᴍ ʙᴇʟᴏᴡ.

from InsaneRobot import pbot as alex # This is bot's client
from pyrogram import filters # pyrogram filters



#ғᴏʀ /help ᴍᴇɴᴜ
__mod_name__ = "Module Name"
__help__ = "Module help message"


@alex.on_message(filters.command("start"))
async def some_function(_, message):
    await message.reply_text("ɪ'ᴍ.ᴀʟɪᴠᴇ ʙᴀʙʏ❣️!!")

# ᴍᴀɴʏ ᴜsᴇғᴜʟ ғᴜɴᴄᴛɪᴏɴs ᴀʀᴇ ɪɴ, InsaneRobot/utils/,InsaneRobot, and InsaneRobot/modules/
```
<h3 align="center"> 
 ᴀɴᴅ ᴘᴜᴛ ᴛʜɪs ғɪʟᴇ ɪɴ InsaneRobot/modules/, ʀᴇsᴛᴀʀᴛ ᴀɴᴅ ᴛᴇsᴛ ʏᴏᴜʀ ʙᴏᴛ.
</h3>
━━━━━━━━━━━━━━━━━━━━
### ㅤㅤㅤㅤᴄʀᴇᴅɪᴛs 

[ᴍᴜᴋᴇsʜ](https://t.me/legend_coder)
 [ᴀɴᴏɴʏᴍᴏᴜs](https://telegram.me/anonymous_was_bot)  
<b>ᴀɴᴅ ᴀʟʟ [ᴛʜᴇ ᴄᴏɴᴛʀɪʙᴜᴛᴏʀs](https://github.com/Noob-Mukesh/MukeshRobot/graphs/contributors) ᴡʜᴏ ʜᴇʟᴩᴇᴅ ❤️ </b>

━━━━━━━━━━━━━━━━━━━━
