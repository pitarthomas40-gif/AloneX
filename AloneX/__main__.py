# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of AloneXMusic


import asyncio
import importlib

from pyrogram import idle

from AloneX import (anon, app, config, db,
                   logger, stop, userbot, yt)
from AloneX.plugins import all_modules
import os
import threading
from flask import Flask

# Flask का अलग नाम रखें ताकि Bot के 'app' से न टकराए
web_app = Flask(__name__)

@web_app.route('/')
def health_check():
    return "Bot is alive and running!"

def run_server():
    # Render डिफ़ॉल्ट रूप से 10000 पोर्ट इस्तेमाल करता है
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

# Flask को एक अलग धागे (Thread) में चलाएं
threading.Thread(target=run_server, daemon=True).start()

# --- इसके नीचे आपका बॉट शुरू करने वाला असली कोड रहेगा ---
# उदाहरण के लिए: 
# asyncio.get_event_loop().run_until_complete(main())

  

async def main():
    await db.connect()
    await app.boot()
    await userbot.boot()
    await anon.boot()

    for module in all_modules:
        importlib.import_module(f"AloneX.plugins.{module}")
    logger.info(f"Loaded {len(all_modules)} modules.")

    if config.COOKIES_URL:
        await yt.save_cookies(config.COOKIES_URL)

    sudoers = await db.get_sudoers()
    app.sudoers.update(sudoers)
    app.bl_users.update(await db.get_blacklisted())
    logger.info(f"Loaded {len(app.sudoers)} sudo users.")

    await idle()
    await stop()


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        pass
