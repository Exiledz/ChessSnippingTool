import os
import sys
import argparse
import subprocess
import webbrowser
import re

parser = argparse.ArgumentParser(description="Image to lichess.")
parser.add_argument("--img", type=str, help="A png file with a chess board")
parser.add_argument("--text", type=str, help="A text file with `black to move` or `white to move`")
parser.add_argument(
    "--tensorflow_chessbot", type=str,
    default=r".\tensorflow_chessbot\tensorflow_chessbot.py", help="a path to tensorflow chessbot")
parser.add_argument("--browser", type=str, default=r'windows-default', help="The name of the web browser to use.")

args = parser.parse_args()

cmdline = ["python", os.path.abspath(args.tensorflow_chessbot), "--filepath=%s" % args.img]
process = subprocess.Popen(
        cmdline, cwd=os.path.dirname(args.tensorflow_chessbot),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if stderr:
    sys.stderr.write(stderr.decode("UTF-8"))
    sys.stderr.write('\n')
    sys.stderr.write("Repro: " + ' '.join(cmdline))
    sys.exit(1)
fen=re.search(r"Predicted FEN:\r\n([^\r]*)", stdout.decode("UTF-8"), flags=re.MULTILINE).group(1)
print(fen)
webbrowser.get(using=args.browser).open("https://lichess.org/analysis/%s" % fen)
