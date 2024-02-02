from Manager import manager
import argparse

parser = argparse.ArgumentParser(description="Файл с задачами")
parser.add_argument('file', type=str)
args = parser.parse_args() #за эти три строчки спасибо Авдееву Жене

manager(args.file, "history.txt")
