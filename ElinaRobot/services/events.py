import inspect
import re
from pathlib import Path

from telethon import events

from ElinaRobot.services.mongo import mongodb as db
from ElinaRobot.services.telethon import tbot

gbanned = db.gban
CMD_LIST = {}


def register(**args):
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
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
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
                # print("i don't work in channels")
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

        tbot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator


def chataction(**args):
    """𝚁𝙴𝙶𝙸𝚂𝚃𝙴𝚁𝚂 𝙲𝙷𝙰𝚃 𝙰𝙲𝚃𝙸𝙾𝙽𝚂."""

    def decorator(func):
        tbot.add_event_handler(func, events.ChatAction(**args))
        return func

    return decorator


def userupdate(**args):
    """𝚁𝙴𝙶𝙸𝚂𝚃𝙴𝚁𝚂 𝚄𝚂𝙴𝚁 𝚄𝙿𝙳𝙰𝚃𝙴𝚂."""

    def decorator(func):
        tbot.add_event_handler(func, events.UserUpdate(**args))
        return func

    return decorator


def inlinequery(**args):
    """𝚁𝙴𝙶𝙸𝚂𝚃𝙴𝚁𝚂 𝙸𝙽𝙻𝙸𝙽𝙴 𝚀𝚄𝙴𝚁𝚈."""
    pattern = args.get("pattern", None)

    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    def decorator(func):
        tbot.add_event_handler(func, events.InlineQuery(**args))
        return func

    return decorator


def callbackquery(**args):
    """𝚁𝙴𝙶𝙸𝚂𝚃𝙴𝚁𝚂 𝙸𝙽𝙻𝙸𝙽𝙴 𝚀𝚄𝙴𝚁𝚈."""

    def decorator(func):
        tbot.add_event_handler(func, events.CallbackQuery(**args))
        return func

    return decorator
