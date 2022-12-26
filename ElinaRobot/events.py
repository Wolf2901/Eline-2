import inspect
import glob
import logging
import sys
import re

from pathlib import Path
from telethon import events

from pymongo import MongoClient
from ElinaRobot import MONGO_DB_URI
from ElinaRobot import telethn

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["ElinaRobot"]
gbanned = db.gban

def register(**args):
    """ 𝚁𝙴𝙶𝙸𝚂𝚃𝙴𝚁 𝙰 𝙽𝙴𝚆 𝙼𝙴𝚂𝚂𝙰𝙶𝙴𝚂. """
    pattern = args.get("pattern", None)

    r_pattern = r"^[/!]"

    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    args["pattern"] = pattern.replace("^/", r_pattern, 1)

    def decorator(func):
        telethn.add_event_handler(func, events.NewMessage(**args))
        return func

    return decorator


def chataction(**args):
    """ 𝚁𝙴𝙶𝙸𝚂𝚃𝙴𝚁𝚂 𝙲𝙷𝙰𝚃 𝙰𝙲𝚃𝙸𝙾𝙽𝚂. """

    def decorator(func):
        telethn.add_event_handler(func, events.ChatAction(**args))
        return func

    return decorator


def userupdate(**args):
    """ 𝚁𝙴𝙶𝙸𝚂𝚃𝙴𝚁𝚂 𝚄𝚂𝙴𝚁 𝚄𝙿𝙳𝙰𝚃𝙴𝚂. """

    def decorator(func):
        telethn.add_event_handler(func, events.UserUpdate(**args))
        return func

    return decorator


def inlinequery(**args):
    """ 𝚁𝙴𝙶𝙸𝚂𝚃𝙴𝚁𝚂 𝙸𝙽𝙻𝙸𝙽𝙴 𝚀𝚄𝙴𝚁𝚈. """
    pattern = args.get("pattern", None)

    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    def decorator(func):
        telethn.add_event_handler(func, events.InlineQuery(**args))
        return func

    return decorator


def callbackquery(**args):
    """ 𝚁𝙴𝙶𝙸𝚂𝚃𝙴𝚁𝚂 𝙸𝙽𝙻𝙸𝙽𝙴 𝚀𝚄𝙴𝚁𝚈. """

    def decorator(func):
        telethn.add_event_handler(func, events.CallbackQuery(**args))
        return func

    return decorator


def bot(**args):
    pattern = args.get("pattern")
    r_pattern = r"^[/]"

    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    args["pattern"] = pattern.replace("^/", r_pattern, 1)
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    reg = re.compile("(.*)")

    if pattern is not None:
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = cmd.group(1).replace("$", "").replace("\\", "").replace("^", "")
            except BaseException:
                pass

            try:
                FUN_LIST[file_test].append(cmd)
            except BaseException:
                FUN_LIST.update({file_test: [cmd]})
        except BaseException:
            pass

    def decorator(func):
        async def wrapper(check):
            if check.edit_date:
                return
            if check.fwd_from:
                return
            if check.is_group or check.is_private:
                pass
            else:
                print("» ɪ ᴅᴏɴ'ᴛ ᴡᴏʀᴋ ɪɴ ᴄʜᴀɴɴᴇʟ....")
                return
            if check.is_group:
               if check.chat.megagroup:
                  pass
               else:
                  print("» ɪ ᴅᴏɴ'ᴛ ᴡᴏʀᴋ ɪɴ sᴍᴀʟʟ ᴄʜᴀᴛs...")
                  return
                          
            users = gbanned.find({})
            for c in users:
                if check.sender_id == c["user"]:
                    return
            try:
                await func(check)
                try:
                    LOAD_PLUG[file_test].append(func)
                except Exception:
                    LOAD_PLUG.update({file_test: [func]})
            except BaseException:
                return
            else:
                pass

        telethn.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator


def ElinaRobot(**args):
    pattern = args.get("pattern", None)
    disable_edited = args.get("disable_edited", False)
    ignore_unsafe = args.get("ignore_unsafe", False)
    unsafe_pattern = r"^[^/!#@\$A-Za-z]"
    group_only = args.get("group_only", False)
    disable_errors = args.get("disable_errors", False)
    insecure = args.get("insecure", False)
    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    if "disable_edited" in args:
        del args["disable_edited"]

    if "ignore_unsafe" in args:
        del args["ignore_unsafe"]

    if "group_only" in args:
        del args["group_only"]

    if "disable_errors" in args:
        del args["disable_errors"]

    if "insecure" in args:
        del args["insecure"]

    if pattern:
        if not ignore_unsafe:
            args["pattern"] = args["pattern"].replace("^.", unsafe_pattern, 1)


def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import importlib
        import ElinaRobot.events

        path = Path(f"ElinaRobot/modules/{shortname}.py")
        name = "ElinaRobot.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("Successfully imported " + shortname)
    else:
        import importlib
        import ElinaRobot.events

        path = Path(f"ElinaRobot/modules/{shortname}.py")
        name = "ElinaRobot.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.register = register
        mod.ElinaRobot = ElinaRobot
        mod.tbot = telethn
        mod.logger = logging.getLogger(shortname)
        spec.loader.exec_module(mod)
        sys.modules["ElinaRobot.modules." + shortname] = mod
        print("Successfully imported " + shortname)


path = "ElinaRobot/modules/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))
