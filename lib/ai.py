import os
import sys
import json
import subprocess
import multiprocessing

try:
    from . import utils
except ImportError:
    import utils

LIBDIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(LIBDIR, "models.json"), "r") as f:
    MODELS = json.load(f)
MODEL = MODELS["models"][MODELS["to_use"]]

LLAMAFILE_ARGS = [
    "-ngl 999",
    "--log-disable",
    "-t {}".format(max(1, multiprocessing.cpu_count() - 1)),
    "--no-display-prompt",
    # "--no-penalize-nl",
    # "--simple-io",
]

LLAMAFILE_ARGS.extend([f"--{opt} {val}" for opt, val in MODELS["options"].items()])

AI_NAME = "Aicha"
USER_NAME = os.getlogin().capitalize()

MODEL_PRE_PROMPT = f"""
This is a conversation between {USER_NAME} and {AI_NAME}, a friendly chatbot.
{AI_NAME} provide very readable, very precise, short and useful answers.
The answers do not contain any text not related to the question
"""

import urllib.request

def download_model(fpath):
    print("\033[?25l", end="")
    urllib.request.urlretrieve(MODEL["url"], fpath, reporthook=utils.dispbar)
    print("\033[?25h")
    os.chmod(fpath, mode=500)

class AiAssistant:
    def __init__(self, data_dir):
        os.makedirs(data_dir, exist_ok=True)
        self.model_path = os.path.join(
            data_dir,
            MODEL["name"].lower().replace(" ", "_")
        ) + ".llamafile"

        if not os.path.isfile(self.model_path):
            res = input("Model {} doesn't exist, download it from Github ? [Y/n] "
                .format(MODEL["name"]))
            if res == "" or res.lower() == "y":
                download_model(self.model_path)
            else:
                sys.exit(0)

    def ask(self, prompt, history=[], maxwidth=100):
        if not prompt or prompt == "":
            print("No question asked")
            return None
        histstr = ""
        for (q, a) in history:
            histstr += f"{USER_NAME}: {q}\n{AI_NAME}: {a}\n"
        final_prompt = f"{MODEL_PRE_PROMPT}\n\n{histstr}{USER_NAME}: {prompt}\n{AI_NAME}: "
        final_prompt = MODEL["prefix"] + utils.sanitize(final_prompt) + MODEL["suffix"]

        result = ""
        env = os.environ.copy()
        env["HIP_VISIBLE_DEVICES"] = "0"
        process = subprocess.Popen(
            "{} {} -p $'{}'".format(
                self.model_path,
                " ".join(LLAMAFILE_ARGS),
                final_prompt
            ),
            executable="bash",
            stdout=subprocess.PIPE,
            env=env,
            encoding="utf-8",
            shell=True,
        )
        try:
            lwidth = 0
            for c in iter(lambda: process.stdout.read(1), ""):
                lwidth += 1
                if c.isspace() and c != "\n" and lwidth >= maxwidth:
                    sys.stdout.write("\n")
                    result += "\n"
                    lwidth = 1
                sys.stdout.write(c)
                sys.stdout.flush()
                result += c
        except KeyboardInterrupt:
            process.kill()
            print("")
        return result

    def save_conversation(self, history):
        pass

    def conversation(self):
        history = []
        print(f"Start of conversation with {AI_NAME}, press CTRL + C to stop")
        while True:
            try:
                prompt = input("> ")
                print("")
            except KeyboardInterrupt:
                self.save_conversation(history)
                break;
            answer = self.ask(prompt, history=history)
            history.append((prompt, answer))
            print("")

    def act(self, args):
        if args.conversation:
            self.conversation()
        elif len(args.question) > 0:
            self.ask(" ".join(args.question))
        else:
            print(f"Either enter a conversation with {AI_NAME}, or ask a single question")

def setup(subp):
    subp.add_argument(
          "--conversation",
          "-c",
          action='store_true',
          help="Begin a conversation instead of asking a single question",
    )

    subp.add_argument("question", help="Question to ask to the AI", nargs="*")

def autocomplete(args):
    pass