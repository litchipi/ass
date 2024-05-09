import os
import sys
import math
import urllib

def sanitize(s):
    s = s.replace("\"", "\\\"").replace("`", "\\`")
    s = s.replace("'", "\\'")
    return s

def stream_command_output(cmd):
    print(cmd)
    print(shlex.split(cmd))

def dispbar(nb, sz, tot, size=None, chars="▐▓▒░▌", ret=True, end=""):
    hide_cursor()
    if not size:
        size = os.get_terminal_size().columns
    nchars = size - 2

    nchunks = math.ceil(tot / sz)
    if nchunks >= size:
        div = nchunks / size
        nb = int(nb / div) + 1
    else:
        mult = size / nchunks
        nb = int(nb * mult) + 1

    if nb < nchars:
        print("{}{}{}{}{}".format(
            chars[0],
            chars[1] * (nb - 1),
            chars[2],
            chars[3] * (nchars - nb),
            chars[4],
        ), end="")
    else:
        print("{}{}{}{}".format(
            chars[0],
            chars[1] * (nchars - 1),
            chars[2],
            chars[4],
        ), end="")
    if ret:
        print("\r", end="")
    print("", end=end)

def download_file(url, fpath, mode=400):
    if os.path.isfile(fpath):
        raise Exception(f"File {fpath} already exists")

    os.makedirs(os.path.dirname(fpath), exist_ok=True)
    try:
        hide_cursor()
        urllib.request.urlretrieve(url, fpath, reporthook=dispbar)
        show_cursor()
    except Exception as err:
        print("")
        show_cursor()
        print(f"Error while downloading {fpath}")
        print(err)
        sys.exit(1)
    except KeyboardInterrupt:
        print("")
        show_cursor()
        print("Interrupted")
        os.remove(fpath)
        sys.exit(1)

    erase_line()
    os.chmod(fpath, mode=mode)

def download_if_not_found(fpath, url, not_found_question, **kwargs):
    if not os.path.isfile(fpath):
        if yes_no_ask(not_found_question):
            download_file(url, fpath, **kwargs)
            erase_line()
            return True
        else:
            return False
    else:
        return True

def erase_line():
    print("\r\033[2K", end="")

def hide_cursor():
    print("\033[?25l", end="")

def show_cursor():
    print("\033[?25h", end="")

def move_cursor(dir, nb):
    if dir == "up":
        print(f"\033[{nb}A", end="")
    elif dir == "down":
        print(f"\033[{nb}B", end="")
    elif dir == "left":
        print(f"\033[{nb}C", end="")
    elif dir == "right":
        print(f"\033[{nb}D", end="")
    else:
        raise Exception(f"Direction {dir} not supported")

def reset_screen():
    show_cursor()
    os.system("reset")

def yes_no_ask(question, default_yes=True, else_is_false=True):
    if default_yes:
        tail = "[Y/n]"
    else:
        tail = "[y/N]"
    i = input(question + " " + tail)
    move_cursor("up", 1)
    erase_line()
    if i == "":
        return default_yes
    elif i.lower() == "y":
        return True
    elif i.lower() == "n":
        return False
    elif else_is_false:
        return False
    else:
        print("Expected \"y\" or \"n\"")
        return yes_no_ask(question, default_yes=default_yes, else_is_false=else_is_false)

def render_duration(nbsecs):
    hours, remainder = divmod(nbsecs, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return "{:.0f} h {:.0f} min {:.0f} secs".format(hours, minutes, seconds)
    elif minutes > 0:
        return "{:.0f} min {:.0f} secs".format(minutes, seconds)
    else:
        return "{:.0f} secs".format(seconds)
