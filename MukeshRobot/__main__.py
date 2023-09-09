import importlib
import re
import time
import asyncio

from telethon import __version__ as tlhver
from platform import python_version as y
from sys import argv

from pyrogram import __version__ as pyrover
from telegram import __version__ as telever
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import (BadRequest, ChatMigrated, NetworkError, TelegramError, TimedOut, Unauthorized, )
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler, Filters, MessageHandler, )
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown
from telethon import __version__ as tlhver

from MukeshRobot import (BOT_NAME, BOT_USERNAME, LOGGER, OWNER_ID, START_IMG, SUPPORT_CHAT, TOKEN, StartTime,
						 dispatcher, pbot, telethn, updater, )
from MukeshRobot.modules import ALL_MODULES
from MukeshRobot.modules.helper_funcs.chat_status import is_user_admin
from MukeshRobot.modules.helper_funcs.misc import paginate_modules


def get_readable_time(seconds: int) -> str:
	count = 0
	ping_time = ""
	time_list = []
	time_suffix_list = ["s", "m", "h", "days"]

	while count < 4:
		count += 1
		remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
		if seconds == 0 and remainder == 0:
			break
		time_list.append(int(result))
		seconds = int(remainder)

	for x in range(len(time_list)):
		time_list[x] = str(time_list[x]) + time_suffix_list[x]
	if len(time_list) == 4:
		ping_time += time_list.pop() + ", "

	time_list.reverse()
	ping_time += ":".join(time_list)

	return ping_time


PM_START_TEX = """
🍷Wᴇʟᴄᴏᴍᴇ `{}`,  🥀 
"""

PM_START_TEXT = """ 
ʜᴇʏ {}, 🥀
*๏ ɪᴛ's ᴍᴇ* 𝑰𝑵𝑺𝑨𝑵𝑬 𝒙 𝑴𝑼𝑺𝑰𝑪✨✨ !

» ᴛʜᴇ ᴍᴏsᴛ ɪɴᴄʀᴇᴅɪʙʟᴇ ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛ ғᴏʀ
✧────────────────✧
                ⁣☼ ɢʀᴏᴜᴩ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ☼
⁣                       ⁣⁣♪ ᴘʟᴀʏ ᴍᴜsɪᴄ ♪
✧────────────────✧
ᴡɪᴛʜ ᴍᴀɴʏ ᴍᴏʀᴇ ᴀᴡᴇsᴏᴍᴇ ᴀɴᴅ ᴜsᴇғᴜʟ ғᴇᴀᴛᴜʀᴇs ғᴏʀ ʏᴏᴜʀ ɢʀᴏᴜᴘs...♡

▼ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ʟᴇᴀʀɴ ᴍᴏʀᴇ !
"""

buttons = [
	[InlineKeyboardButton(text="💫 ᴛᴇʟᴇᴘᴏʀᴛ ᴍᴇ 💫", url=f"https://t.me/{dispatcher.bot.username}?startgroup=true", ), ],
	[InlineKeyboardButton(text="🌟 ᴍᴀɴᴀɢᴇᴍᴇɴᴛ 🌟", callback_data="help_back"),
		InlineKeyboardButton(text="🎧 ᴍᴜsɪᴄ 🎧", callback_data="Music_"), ],
	[InlineKeyboardButton(text="💜 sᴜᴩᴩᴏʀᴛ 💜", url="https://t.me/tofani_support"),

	],

]

HELP_STRINGS = """
[𝑰𝑵𝑺𝑨𝑵𝑬 𝒙 𝑴𝑼𝑺𝑰𝑪✨✨](tg://user?id=6019282272)
» ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ᴀʙᴏᴜᴛ sᴘᴇᴄɪғɪᴄs ᴄᴏᴍᴍᴀɴᴅ.
"""

DONATE_STRING = """ʜᴇʏ ʙᴀʙʏ, 🤍
  ʜᴀᴩᴩʏ ᴛᴏ ʜᴇᴀʀ ᴛʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴅᴏɴᴀᴛᴇ.

ʏᴏᴜ ᴄᴀɴ ᴅɪʀᴇᴄᴛʟʏ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ [ᴅᴇᴠᴇʟᴏᴩᴇʀ](https://t.me/pyal3x) ғᴏʀ ᴅᴏɴᴀᴛɪɴɢ ᴏʀ ʏᴏᴜ ᴄᴀɴ ᴠɪsɪᴛ ᴍʏ [sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ](https://t.me/tofani_support) ᴀɴᴅ ᴀsᴋ ᴛʜᴇʀᴇ ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪᴏɴ."""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
	imported_module = importlib.import_module("MukeshRobot.modules." + module_name)
	if not hasattr(imported_module, "__mod_name__"):
		imported_module.__mod_name__ = imported_module.__name__

	if imported_module.__mod_name__.lower() not in IMPORTED:
		IMPORTED[imported_module.__mod_name__.lower()] = imported_module

	if hasattr(imported_module, "__help__") and imported_module.__help__:
		HELPABLE[imported_module.__mod_name__.lower()] = imported_module

	# Chats to migrate on chat_migrated events
	if hasattr(imported_module, "__migrate__"):
		MIGRATEABLE.append(imported_module)

	if hasattr(imported_module, "__stats__"):
		STATS.append(imported_module)

	if hasattr(imported_module, "__user_info__"):
		USER_INFO.append(imported_module)

	if hasattr(imported_module, "__import_data__"):
		DATA_IMPORT.append(imported_module)

	if hasattr(imported_module, "__export_data__"):
		DATA_EXPORT.append(imported_module)

	if hasattr(imported_module, "__chat_settings__"):
		CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

	if hasattr(imported_module, "__user_settings__"):
		USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
	if not keyboard:
		keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
	dispatcher.bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN,
		disable_web_page_preview=True, reply_markup=keyboard, )


@run_async
def test(update: Update, context: CallbackContext):
	# pprint(eval(str(update)))
	update.effective_message.reply_text("Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN)
	update.effective_message.reply_text("This person edited a message")
	print(update.effective_message)


@run_async
def start(update: Update, context: CallbackContext):
	args = context.args
	uptime = get_readable_time((time.time() - StartTime))
	if update.effective_chat.type == "private":
		if len(args) >= 1:
			if args[0].lower() == "help":
				send_help(update.effective_chat.id, HELP_STRINGS)
			elif args[0].lower().startswith("ghelp_"):
				mod = args[0].lower().split("_", 1)[1]
				if not HELPABLE.get(mod, False):
					return
				send_help(update.effective_chat.id, HELPABLE[mod].__help__,
					InlineKeyboardMarkup([[InlineKeyboardButton(text="🔙", callback_data="help_back")]]), )

			elif args[0].lower().startswith("stngs_"):
				match = re.match("stngs_(.*)", args[0].lower())
				chat = dispatcher.bot.getChat(match.group(1))

				if is_user_admin(chat, update.effective_user.id):
					send_settings(match.group(1), update.effective_user.id, False)
				else:
					send_settings(match.group(1), update.effective_user.id, True)

			elif args[0][1:].isdigit() and "rules" in IMPORTED:
				IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

		else:
			first_name = update.effective_user.first_name

			usr = update.effective_user
			lol = update.effective_message.reply_text(PM_START_TEX.format(usr.first_name),
				parse_mode=ParseMode.MARKDOWN)
			time.sleep(0.3)
			lol.edit_text("❤️")
			time.sleep(0.2)
			lol.edit_text("⚡")
			time.sleep(0.2)
			lol.edit_text("ꜱᴛᴀʀᴛɪɴɢ.")
			time.sleep(0.2)
			lol.edit_text("ꜱᴛᴀʀᴛɪɴɢ..")
			time.sleep(0.2)
			lol.edit_text("ꜱᴛᴀʀᴛɪɴɢ...")
			time.sleep(0.2)
			lol.delete()
			update.effective_message.reply_sticker(
				"CAACAgEAAxkBAAEBp39k4Ju_jjTgvHMxokxe9HE8TJMrnAACkwQAAnwMAAFHB1BeBi72KxwwBA")
			update.effective_message.reply_text(
				PM_START_TEXT.format(escape_markdown(first_name), (START_IMG), BOT_NAME),
				reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.MARKDOWN, timeout=60, )
	else:
		update.effective_message.reply_photo(START_IMG,
			caption="ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ  !\n<b>ɪ ᴅɪᴅɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ​:</b> <code>{}</code>".format(uptime),
			parse_mode=ParseMode.HTML, )


def error_handler(update, context):
	"""Log the error and send a telegram message to notify the developer."""
	# Log the error before we do anything else, so we can see it even if something breaks.
	LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

	# traceback.format_exception returns the usual python message about an exception, but as a
	# list of strings rather than a single string, so we have to join them together.
	tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
	tb = "".join(tb_list)

	# Build the message with some markup and additional information about what happened.
	message = ("An exception was raised while handling an update\n"
			   "<pre>update = {}</pre>\n\n"
			   "<pre>{}</pre>").format(html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
		html.escape(tb), )

	if len(message) >= 4096:
		message = message[:4096]
	# Finally, send the message
	context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
	error = context.error
	try:
		raise error
	except Unauthorized:
		print("no nono1")
		print(error)  # remove update.message.chat_id from conversation list
	except BadRequest:
		print("no nono2")
		print("BadRequest caught")
		print(error)

	# handle malformed requests - read more below!
	except TimedOut:
		print("no nono3")  # handle slow connection problems
	except NetworkError:
		print("no nono4")  # handle other connection problems
	except ChatMigrated as err:
		print("no nono5")
		print(err)  # the chat_id of a group has changed, use e.new_chat_id instead
	except TelegramError:
		print(error)  # handle all other telegram related errors


@run_async
def help_button(update, context):
	query = update.callback_query
	mod_match = re.match(r"help_module\((.+?)\)", query.data)
	prev_match = re.match(r"help_prev\((.+?)\)", query.data)
	next_match = re.match(r"help_next\((.+?)\)", query.data)
	back_match = re.match(r"help_back", query.data)

	print(query.message.chat.id)

	try:
		if mod_match:
			module = mod_match.group(1)
			text = ("» *ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ​​* *{}* :\n".format(HELPABLE[module].__mod_name__) + HELPABLE[
				module].__help__)
			query.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True,
				reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="🔙", callback_data="help_back")]]), )

		elif prev_match:
			curr_page = int(prev_match.group(1))
			query.message.edit_text(text=HELP_STRINGS, parse_mode=ParseMode.MARKDOWN,
				reply_markup=InlineKeyboardMarkup(paginate_modules(curr_page - 1, HELPABLE, "help")), )

		elif next_match:
			next_page = int(next_match.group(1))
			query.message.edit_text(text=HELP_STRINGS, parse_mode=ParseMode.MARKDOWN,
				reply_markup=InlineKeyboardMarkup(paginate_modules(next_page + 1, HELPABLE, "help")), )

		elif back_match:
			query.message.edit_text(text=HELP_STRINGS, parse_mode=ParseMode.MARKDOWN,
				reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help")), )

		# ensure no spinny white circle
		context.bot.answer_callback_query(query.id)  # query.message.delete()

	except BadRequest:
		pass


@run_async
def mukesh_about_callback(update: Update, context: CallbackContext):
	query = update.callback_query
	if query.data == "alex_":
		uptime = get_readable_time((time.time() - StartTime))
		query.message.edit_text(text=f"*ʜᴇʏ,*🥀\n  *ᴛʜɪs ɪs {dispatcher.bot.first_name}*"
									 "\n\n*ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ & ᴍᴜsɪᴄ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴜɪʟᴛ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴇᴀꜱɪʟʏ ᴀɴᴅ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ʏᴏᴜʀ ɢʀᴏᴜᴘ ꜰʀᴏᴍ ꜱᴄᴀᴍᴍᴇʀꜱ ᴀɴᴅ ꜱᴘᴀᴍᴍᴇʀꜱ.*"
									 "\n*ᴡʀɪᴛᴛᴇɴ ɪɴ ᴩʏᴛʜᴏɴ ᴡɪᴛʜ sǫʟᴀʟᴄʜᴇᴍʏ ᴀɴᴅ ᴍᴏɴɢᴏᴅʙ ᴀs ᴅᴀᴛᴀʙᴀsᴇ.*"
									 "\n➲  ɪ ᴄᴀɴ ʀᴇꜱᴛʀɪᴄᴛ ᴜꜱᴇʀꜱ."
									 "\n➲  ɪ ʜᴀᴠᴇ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴛɪ-ꜰʟᴏᴏᴅ ꜱʏꜱᴛᴇᴍ."
									 "\n➲  ɪ ᴄᴀɴ ɢʀᴇᴇᴛ ᴜꜱᴇʀꜱ ᴡɪᴛʜ ᴄᴜꜱᴛᴏᴍɪᴢᴀʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇꜱꜱᴀɢᴇꜱ ᴀɴᴅ ᴇᴠᴇɴ ꜱᴇᴛ ᴀ ɢʀᴏᴜᴘ'ꜱ ʀᴜʟᴇꜱ."
									 "\n➲  ɪ ᴄᴀɴ ᴡᴀʀɴ ᴜꜱᴇʀꜱ ᴜɴᴛɪʟ ᴛʜᴇʏ ʀᴇᴀᴄʜ ᴍᴀx ᴡᴀʀɴꜱ, ᴡɪᴛʜ ᴇᴀᴄʜ ᴘʀᴇᴅᴇꜰɪɴᴇᴅ ᴀᴄᴛɪᴏɴꜱ ꜱᴜᴄʜ ᴀꜱ ʙᴀɴ, ᴍᴜᴛᴇ, ᴋɪᴄᴋ, ᴇᴛᴄ."
									 "\n➲  ɪ ʜᴀᴠᴇ ᴀ ɴᴏᴛᴇ ᴋᴇᴇᴘɪɴɢ ꜱʏꜱᴛᴇᴍ, ʙʟᴀᴄᴋʟɪꜱᴛꜱ, ᴀɴᴅ ᴇᴠᴇɴ ᴘʀᴇᴅᴇᴛᴇʀᴍɪɴᴇᴅ ʀᴇᴘʟɪᴇꜱ ᴏɴ ᴄᴇʀᴛᴀɪɴ ᴋᴇʏᴡᴏʀᴅꜱ.",
			parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([
				[InlineKeyboardButton(text="oᴡɴᴇʀ", url=f"tg://user?id={OWNER_ID}"),
					InlineKeyboardButton(text="support", url="https://t.me/tofani_support"), ],
				[InlineKeyboardButton(text="🔙", callback_data="alex_back"), ], ]), )
	elif query.data == "alex_back":
		first_name = update.effective_user.first_name
		query.message.edit_text(PM_START_TEXT.format(escape_markdown(first_name), (START_IMG), BOT_NAME),
			reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.MARKDOWN, timeout=60,
			disable_web_page_preview=False, )


@run_async
def Music_about_callback(update: Update, context: CallbackContext):
	query = update.callback_query
	if query.data == "Music_":
		query.message.edit_text(text="*Help ⚙️*\n\n"
									 "__» All commands are categorized based on their usability and target users.__\n"
									 "__» You can use these buttons below to navigate each category and get respective commands.__\n"
									 "__» Feel free to contact us if you need any help regarding the bot.__\n\n"
									 "❤️🎶 [𝑰𝑵𝑺𝑨𝑵𝑬 𝒙 𝑴𝑼𝑺𝑰𝑪✨✨](t.me/insane_xmusic_bot)", parse_mode=ParseMode.MARKDOWN,
			disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([
				[InlineKeyboardButton(text="➊ Admins", callback_data="Music_1"),
				 InlineKeyboardButton(text="➋ Users", callback_data="Music_2"), ],
				[InlineKeyboardButton(text="➌ Sudos", callback_data="Music_3"),
					InlineKeyboardButton(text="➍ Others", callback_data="Music_4"), ],
				[InlineKeyboardButton(text="➎ Owner", callback_data="Music_5"), ],
				[InlineKeyboardButton(text="🔙", callback_data="alex_back"), ], ]), )
	elif query.data == "Music_1":
		query.message.edit_text(text="*Authorized Users Commands:*\n\n"
									 "*» /auth ; /unauth*\n"
									 "    __Authorize or unauthorize user to use admins command such as /skip, /pause, etc.__\n\n"
									 "*» /authlist*\n"
									 "    __List all authorized users.__\n\n"
									 "*» /authchat*\n"
									 "    __This enables all the users in the chat to use admins command such as /skip, /pause, etc.__\n\n"
									 "*» /mute ; /unmute*\n"
									 "    __Mute or unmute the ongoing track in the voice chat.__\n\n"
									 "*» /pause ; /resume*\n"
									 "    __Pause or resume the ongoing track in the voice chat.__\n\n"
									 "*» /stop ; /end*\n"
									 "    __Stop the ongoing track in the voice chat.__\n\n"
									 "*» /loop*\n"
									 "    __Loop the playing track in the voice chat. Use [/loop 0] to disable the loop.__\n\n"
									 "*» /skip*\n"
									 "    __Skip the playing track in the voice chat.__\n\n"
									 "*» /replay*\n"
									 "    __Replay from the beginning of the playing track in the voice chat.__\n\n"
									 "*» /seek*\n"
									 "    __Seek the playing track in the voice chat. Use [/seek 10] to seek forward and [/seek-10] to seek backwards.__\n\n"
									 "*» /clean*\n"
									 "    __Clear the queue when bot seems to be bugged.__\n\n",
			parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="🔙", callback_data="Music_"), ]]), )
	elif query.data == "Music_2":
		query.message.edit_text(text="*Normal Users Commands:*\n\n"
									 "*» /play ; /vplay*\n"
									 "    __Play replied audio/video file or youtube video or searched query on voice chat.__\n\n"
									 "*» /fplay ; /fvplay*\n"
									 "    __Force play replied audio/video file or youtube video or searched query on voice chat.__\n\n"
									 "*» /favs ; /myfavs ; /favorites*\n"
									 "    __Show your favorite songs list.__\n\n"
									 "*» /delfavs*\n"
									 "    __Delete your favorite songs from your list.__\n\n"
									 "*» /current ; /playing*\n"
									 "    __Show the current playing song.__\n\n"
									 "*» /queue ; /que ; /q*\n"
									 "    __Show the queued songs list.__\n\n"
									 "*» /song*\n"
									 "    __Download the searched song from youtube.__\n\n"
									 "*» /lyrics*\n"
									 "    __Get the lyrics of the searched song. Give artist name after ' - ' for accurate results. [/lyrics Without Me - Eminem]__\n\n"
									 "*» /profile ; /me*\n"
									 "    __Show your profile and stats.__\n\n", parse_mode=ParseMode.MARKDOWN,
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="🔙", callback_data="Music_"), ]]), )
	elif query.data == "Music_3":
		query.message.edit_text(text="*Sudo Users Commands:*\n\n"
									 "*» /active*\n"
									 "    __Check active voice chats of the bot.__\n\n"
									 "*» /autoend*\n"
									 "    __Enable or disable autoend inactive voice chats.__\n\n"
									 "*» /block ; /unblock*\n"
									 "    __Block or unblock user from using the bot.__\n\n"
									 "*» /blocklist*\n"
									 "    __List all blocked users.__\n\n"
									 "*» /gban ; /ungban*\n"
									 "    __Globally ban or unban user from using the bot.__\n\n"
									 "*» /gbanlist*\n"
									 "    __List all globally banned users.__\n\n"
									 "*» /logs*\n"
									 "    __Get the logs of the bot.__\n\n"
									 "*» /restart*\n"
									 "    __Restart the bot globally.__\n\n"
									 "*» /sudolist*\n"
									 "    __List all sudo users.__\n\n"
									 "*» /stats*\n"
									 "    __Show full stats of the bot.__\n\n", parse_mode=ParseMode.MARKDOWN,
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="🔙", callback_data="Music_"), ]]), )
	elif query.data == "Music_4":
		query.message.edit_text(text="*Other Commands:*\n\n"
									 "*» /start*\n"
									 "    __Check if the bot is alive.__\n\n"
									 "*» /ping*\n"
									 "    __Check ping of the bot.__\n\n"
									 "*» /help*\n"
									 "    __Show this menu.__\n\n"
									 "*» /sysinfo*\n"
									 "    __Show system information of the bot.__\n\n"
									 "*» /leaderboard ; /topusers*\n"
									 "    __Show the top 10 users with most number of songs played.__\n\n",
			parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="🔙", callback_data="Music_"), ]]), )
	elif query.data == "Music_5":
		query.message.edit_text(text="*Owner Commands:*\n\n"
									 "*» /eval ; /run*\n"
									 "    __Execute the python script.__\n\n"
									 "*» /exec ; /term ; /sh*\n"
									 "    __Execute the bash script.__\n\n"
									 "*» /getvar ; /gvar ; /var*\n"
									 "    __Get the value of the config variable.__\n\n"
									 "*» /addsudo*\n"
									 "    __Add sudo user of the bot who can use sudo commands.__\n\n"
									 "*» /rmsudo ; /delsudo*\n"
									 "    __Remove sudo user of the bot.__\n\n", parse_mode=ParseMode.MARKDOWN,
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="🔙", callback_data="Music_"), ]]), )
	elif query.data == "Music_back":
		first_name = update.effective_user.first_name
		query.message.edit_text(PM_START_TEXT.format(escape_markdown(first_name), (START_IMG), BOT_NAME),
			reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.MARKDOWN, timeout=60,
			disable_web_page_preview=False, )


@run_async
def get_help(update: Update, context: CallbackContext):
	chat = update.effective_chat  # type: Optional[Chat]
	args = update.effective_message.text.split(None, 1)

	# ONLY send help in PM
	if chat.type != chat.PRIVATE:
		if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
			module = args[1].lower()
			update.effective_message.reply_text(f"Contact me in PM to get help of {module.capitalize()}",
				reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="📚 ʜᴇʟᴘ 📚",
					url="t.me/{}?start=ghelp_{}".format(context.bot.username, module), )]]), )
			return
		update.effective_message.reply_text("» ᴄʜᴏᴏꜱᴇ ᴀɴ.ᴏᴘᴛɪᴏɴ ꜰᴏʀ ɢᴇᴛᴛɪɴɢ ʜᴇʟᴘ ", reply_markup=InlineKeyboardMarkup([[
			InlineKeyboardButton(text="Sᴛᴀʀᴛ ɪɴ ᴘʀɪᴠᴀᴛᴇ ",
				url="https://t.me/{}?start=help".format(context.bot.username), )],
			[InlineKeyboardButton(text="Oᴘᴇɴ ʜᴇʀᴇ", callback_data="help_back", )], ]), )
		return

	elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
		module = args[1].lower()
		text = ("Here is the available help for the *{}* module:\n".format(HELPABLE[module].__mod_name__) + HELPABLE[
			module].__help__)
		send_help(chat.id, text, InlineKeyboardMarkup([[InlineKeyboardButton(text="🔙", callback_data="help_back")]]), )

	else:
		send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
	if user:
		if USER_SETTINGS:
			settings = "\n\n".join(
				"*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id)) for mod in USER_SETTINGS.values())
			dispatcher.bot.send_message(user_id, "These are your current settings:" + "\n\n" + settings,
				parse_mode=ParseMode.MARKDOWN, )

		else:
			dispatcher.bot.send_message(user_id, "Seems like there aren't any user specific settings available :'(",
				parse_mode=ParseMode.MARKDOWN, )

	else:
		if CHAT_SETTINGS:
			chat_name = dispatcher.bot.getChat(chat_id).title
			dispatcher.bot.send_message(user_id,
				text="Which module would you like to check {}'s settings for?".format(chat_name),
				reply_markup=InlineKeyboardMarkup(paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)), )
		else:
			dispatcher.bot.send_message(user_id, "Seems like there aren't any chat settings available :'(\nSend this "
												 "in a group chat you're admin in to find its current settings!",
				parse_mode=ParseMode.MARKDOWN, )


@run_async
def settings_button(update: Update, context: CallbackContext):
	query = update.callback_query
	user = update.effective_user
	bot = context.bot
	mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
	prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
	next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
	back_match = re.match(r"stngs_back\((.+?)\)", query.data)
	try:
		if mod_match:
			chat_id = mod_match.group(1)
			module = mod_match.group(2)
			chat = bot.get_chat(chat_id)
			text = "*{}* has the following settings for the *{}* module:\n\n".format(escape_markdown(chat.title),
				CHAT_SETTINGS[module].__mod_name__) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
			query.message.reply_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(
				[[InlineKeyboardButton(text="◁", callback_data="stngs_back({})".format(chat_id), )]]), )

		elif prev_match:
			chat_id = prev_match.group(1)
			curr_page = int(prev_match.group(2))
			chat = bot.get_chat(chat_id)
			query.message.reply_text("Hi there! There are quite a few settings for {} - go ahead and pick what "
									 "you're interested in.".format(chat.title), reply_markup=InlineKeyboardMarkup(
				paginate_modules(curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id)), )

		elif next_match:
			chat_id = next_match.group(1)
			next_page = int(next_match.group(2))
			chat = bot.get_chat(chat_id)
			query.message.reply_text("Hi there! There are quite a few settings for {} - go ahead and pick what "
									 "you're interested in.".format(chat.title), reply_markup=InlineKeyboardMarkup(
				paginate_modules(next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id)), )

		elif back_match:
			chat_id = back_match.group(1)
			chat = bot.get_chat(chat_id)
			query.message.reply_text(text="Hi there! There are quite a few settings for {} - go ahead and pick what "
										  "you're interested in.".format(escape_markdown(chat.title)),
				parse_mode=ParseMode.MARKDOWN,
				reply_markup=InlineKeyboardMarkup(paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)), )

		# ensure no spinny white circle
		bot.answer_callback_query(query.id)
		query.message.delete()
	except BadRequest as excp:
		if excp.message not in ["Message is not modified", "Query_id_invalid", "Message can't be deleted", ]:
			LOGGER.exception("Exception in settings buttons. %s", str(query.data))


@run_async
def get_settings(update: Update, context: CallbackContext):
	chat = update.effective_chat  # type: Optional[Chat]
	user = update.effective_user  # type: Optional[User]
	msg = update.effective_message  # type: Optional[Message]

	# ONLY send settings in PM
	if chat.type != chat.PRIVATE:
		if is_user_admin(chat, user.id):
			text = "Click here to get this chat's settings, as well as yours."
			msg.reply_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="sᴇᴛᴛɪɴɢs​",
				url="t.me/{}?start=stngs_{}".format(context.bot.username, chat.id), )]]), )
		else:
			text = "Click here to check your settings."

	else:
		send_settings(chat.id, user.id, True)


@run_async
def donate(update: Update, context: CallbackContext):
	user = update.effective_message.from_user
	chat = update.effective_chat  # type: Optional[Chat]
	bot = context.bot
	if chat.type == "private":
		update.effective_message.reply_text(DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

		if OWNER_ID != {OWNER_ID} and DONATION_LINK:
			update.effective_message.reply_text(
				f"» ᴛʜᴇ ᴅᴇᴠᴇʟᴏᴩᴇʀ ᴏғ {dispatcher.bot.first_name} sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ɪs [Alex](https://t.me/PyAL3X)"
				f"\n\nʙᴜᴛ ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴅᴏɴᴀᴛᴇ ᴛᴏ ᴛʜᴇ ᴩᴇʀsᴏɴ ᴄᴜʀʀᴇɴᴛʟʏ ʀᴜɴɴɪɴɢ ᴍᴇ : [ʜᴇʀᴇ]({DONATION_LINK})",
				parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True, )

	else:
		try:
			bot.send_message(user.id, DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True, )

			update.effective_message.reply_text("ɪ'ᴠᴇ ᴘᴍ'ᴇᴅ ʏᴏᴜ ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪɴɢ ᴛᴏ ᴍʏ ᴄʀᴇᴀᴛᴏʀ!")
		except Unauthorized:
			update.effective_message.reply_text("ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴍ ғɪʀsᴛ ᴛᴏ ɢᴇᴛ ᴅᴏɴᴀᴛɪᴏɴ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.")


def migrate_chats(update: Update, context: CallbackContext):
	msg = update.effective_message  # type: Optional[Message]
	if msg.migrate_to_chat_id:
		old_chat = update.effective_chat.id
		new_chat = msg.migrate_to_chat_id
	elif msg.migrate_from_chat_id:
		old_chat = msg.migrate_from_chat_id
		new_chat = update.effective_chat.id
	else:
		return

	LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
	for mod in MIGRATEABLE:
		mod.__migrate__(old_chat, new_chat)

	LOGGER.info("Successfully migrated!")
	raise DispatcherHandlerStop


def main():
	if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
		try:
			dispatcher.bot.sendAnimation(f"@{SUPPORT_CHAT}",
				animation="https://graph.org/file/541a20ea48a26429a67fc.mp4", caption=f"""
ㅤ🥀 ✨ㅤ{dispatcher.bot.first_name}  is again active af...!

×⋆───────────────⋆×
	*ᴘʏᴛʜᴏɴ :* `{y()}`
	*ʟɪʙʀᴀʀʏ :* `{telever}`
	*ᴛᴇʟᴇᴛʜᴏɴ :* `{tlhver}`
	*ᴩʏʀᴏɢʀᴀᴍ :* `{pyrover}`
×⋆───────────────⋆×

""", parse_mode=ParseMode.MARKDOWN, )
		except Unauthorized:
			LOGGER.warning(f"Bot isn't able to send message to @{SUPPORT_CHAT}, go and check!")
		except BadRequest as e:
			LOGGER.warning(e.message)

	CommandHandler("test", test)
	start_handler = CommandHandler("start", start)

	help_handler = CommandHandler("help", get_help)
	help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_.*")

	settings_handler = CommandHandler("settings", get_settings)
	settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_")

	about_callback_handler = CallbackQueryHandler(mukesh_about_callback, pattern=r"alex_")
	Music_callback_handler = CallbackQueryHandler(Music_about_callback, pattern=r"Music_")

	donate_handler = CommandHandler("donate", donate)
	migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)

	# dispatcher.add_handler(test_handler)
	dispatcher.add_handler(start_handler)
	dispatcher.add_handler(help_handler)
	dispatcher.add_handler(about_callback_handler)
	dispatcher.add_handler(Music_callback_handler)
	dispatcher.add_handler(settings_handler)
	dispatcher.add_handler(help_callback_handler)
	dispatcher.add_handler(settings_callback_handler)
	dispatcher.add_handler(migrate_handler)
	dispatcher.add_handler(donate_handler)

	dispatcher.add_error_handler(error_callback)

	LOGGER.info(
		"!!!BOT IS STARTED SUCCESSFULLY!!!\n\n╔═════ஜ۩۞۩ஜ════╗\n\nENJOY\n\n╚═════ஜ۩۞۩ஜ════╝")
	updater.start_polling(timeout=15, read_latency=4, clean=True)

	if len(argv) not in (1, 3, 4):
		telethn.disconnect()
	else:
		telethn.run_until_disconnected()

	updater.idle()


if __name__ == "__main__":
	LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
	telethn.start(bot_token=TOKEN)
	pbot.start()
	main()
