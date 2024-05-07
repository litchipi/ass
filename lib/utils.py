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
    except KeyboardInterrupt:
        reset_screen()
        print("Interrupted")
        os.remove(fpath)
        sys.exit(1)

    os.chmod(fpath, mode=mode)

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
    print("\033c", end="")
