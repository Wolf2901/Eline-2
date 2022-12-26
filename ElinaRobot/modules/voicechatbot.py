import os
import aiofiles
import aiohttp
from random import randint
from pyrogram import filters
from ElinaRobot import pbot as Elina

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                data = await resp.json()
            except:
                data = await resp.text()
    return data

async def ai_elina(url):
    ai_name = "elina.mp3"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(ai_name, mode="wb")
                await f.write(await resp.read())
                await f.close()
    return ai_name


@Elina.on_message(filters.command("Elina"))
async def Lycia(_, message):
    if len(message.command) < 2:
        await message.reply_text("Elina AI Voice Chatbot")
        return
    text = message.text.split(None, 1)[1]
    Elina = text.replace(" ", "%20")
    m = await message.reply_text("Elina Is Best...")
    try:
        L = await fetch(f"https://api.affiliateplus.xyz/api/chatbot?message={lycia}&botname=amelia&ownername=Abhishek&user=1")
        chatbot = L["message"]
        VoiceAi = f"https://lyciavoice.herokuapp.com/lycia?text={chatbot}&lang=hi"
        name = "elina"
    except Exception as e:
        await m.edit(str(e))
        return
    await m.edit("Made By @Wolf_2904...")
    ElinaVoice = await ai_Elina(VoiceAi)
    await m.edit("Repyping...")
    await message.reply_audio(audio=ElinaVoice, title=chatbot, performer=name)
    os.remove(ElinaVoice)
    await m.delete()
