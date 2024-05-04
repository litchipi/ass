import math

def sanitize(s):
    s = s.replace("\"", "\\\"").replace("`", "\\`")
    s = s.replace("'", "\\'")
    return s

def stream_command_output(cmd):
    print(cmd)
    print(shlex.split(cmd))

def dispbar(nb, sz, tot, size=150, chars="▐▓▒░▌"):
    nchunks = math.ceil(tot / sz)
    div = nchunks / size
    nchars = math.ceil(nchunks / div)
    nb = int(nb / div) + 1
    if nb < nchars:
        print("{}{}{}{}{}\r".format(
            chars[0],
            chars[1] * (nb - 1),
            chars[2],
            chars[3] * (nchars - nb),
            chars[4],
        ), end="")
    else:
        print("{}{}{}{}\r".format(
            chars[0],
            chars[1] * (nchars - 1),
            chars[2],
            chars[4],
        ), end="")
