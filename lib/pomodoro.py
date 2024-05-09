import os
import sys
import time
from pydbus import SessionBus

import subprocess
from subprocess import DEVNULL

try:
    from . import utils
except ImportError:
    import utils

WORK_STATE = 1
PAUSE_STATE = 2

DEFAULT_MUSICS = {
    "work": "https://bigsoundbank.com/UPLOAD/mp3/2687.mp3",
    "pause": "https://bigsoundbank.com/UPLOAD/mp3/2366.mp3",
}

DEFAULT_ICON = "https://inlucro.org/wp-content/uploads/2016/02/pomodoro.png"

class PomodoroTimer:
    def __init__(self, datapath, tasklist=[], nomusic=False, nonotify=False, nowait=False, **args):
        self.data_dir = datapath

        self.icon = os.path.join(self.data_dir, "icon.png")
        if not os.path.isfile(self.icon):
            utils.download_file(DEFAULT_ICON, self.icon)

        self.music = not nomusic
        if self.music:
            self.work_music = os.path.join(self.data_dir, "work_finished.mp3")
            if not utils.download_if_not_found(
               self.work_music,
               DEFAULT_MUSICS["work"],
               "Notification music not found under {}, download ?".format(self.work_music),
           ):
                print("Notification music disabled")
                self.music = False

        if self.music:
            self.pause_music = os.path.join(self.data_dir, "pause_finished.mp3")
            if not utils.download_if_not_found(
               self.pause_music,
               DEFAULT_MUSICS["pause"],
               "Notification music not found under {}, download ?".format(self.pause_music),
           ):
                print("Notification music disabled")
                self.music = False

        self.work = args["work"] * 60
        self.pause = args["pause"] * 60
        self.state = WORK_STATE
        self.tasks = tasklist
        self.task_n = 0
        self.refresh = min(0.5, self.work / 100)
        self.newstate_wait = not nowait
        self.notify = not nonotify
        self.tot_work_done = 0

        self.bus = SessionBus().get(".Notifications")

    def start_cli(self):
        utils.hide_cursor()
        try:
            self.loop()
        except KeyboardInterrupt:
            print("toto")
            utils.reset_screen()
            print("")

    def loop(self):
        self.tstart = time.time()

        self.change_state(WORK_STATE, init=True)
        while True:
            curr = time.time() - self.tstart

            if self.state == WORK_STATE:
                if curr > self.work:
                    self.change_state(PAUSE_STATE)
                    continue

            elif self.state == PAUSE_STATE:
                if curr > self.pause:
                    self.change_state(WORK_STATE)
                    continue

            self.display_screen(curr)
            time.sleep(self.refresh)

    def change_state(self, new_state, init=False):
        music = None
        if not init:
            if new_state == WORK_STATE:
                self.task_n += 1
                self.send_notification("New work session", "Pause finished !")
                music = self.play_music(self.work_music)

            elif new_state == PAUSE_STATE:
                self.tot_work_done += self.work
                self.send_notification("End of work session", "The work session has ended")
                music = self.play_music(self.pause_music)

        utils.erase_line()
        try:
            input("Press enter to start")
        except KeyboardInterrupt:
            utils.reset_screen()
            sys.exit(0)

        if init:
            utils.move_cursor("up", 1)
            utils.erase_line()

        if music:
            music.kill()

        self.state = new_state
        self.tstart = time.time()

    def send_notification(self, title, msg):
        if not self.notify:
            return
        self.bus.Notify(
            'Ass Pomodoro',
            0,
            self.icon,
            title,
            msg,
            [],
            {},
            5000,
        )

    def play_music(self, music):
        if not self.music:
            return
        return subprocess.Popen(["mpg123", music], stdout=DEVNULL, stderr=DEVNULL)

    def display_screen(self, n):
        add_t = 0
        if self.state == WORK_STATE:
            add_t = n

        utils.erase_line()
        print("Time worked:", utils.render_time(self.tot_work_done + add_t))

        utils.erase_line()
        if self.state == WORK_STATE:
            if len(self.tasks) > self.task_n:
                print(self.tasks[self.task_n])
            else:
                print("Work")
        else:
            print("Pause")
    
        if self.state == WORK_STATE:
            t = self.work
        elif self.state == PAUSE_STATE:
            t = self.pause
        else:
            raise Exception("Got unreachable case")

        utils.dispbar(n, 1, t, end="\n", ret=False)
        utils.move_cursor("up", 3)

def setup(subp):
    subp.add_argument("--work", "-w", help="Work time, in minutes", default=40, type=int)
    subp.add_argument("--pause", "-p", help="Pause time, in minutes", default=5, type=int)
    subp.add_argument("--nowait", "-n", help="Do not wait when a new state starts", action="store_true")
    subp.add_argument("--nonotify", "-s", help="Do not notify when a state finishes", action="store_true")
    subp.add_argument("--nomusic", "-m", help="Do not use a music when a state finishes", action="store_true")

def autocomplete(args):
    pass

def act(root, **args):
    return PomodoroTimer(root, **args).start_cli()
