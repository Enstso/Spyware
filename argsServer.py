import argparse
import sys

class ArgumentParser(argparse.ArgumentParser):

    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, sys.stderr)

    def error(self, message):
        raise Exception(message)

def arguments():
    parser = ArgumentParser()
    parser.add_argument("-l", "--listen", metavar='<port>', type=int, help="switch to listen on specified port")
    parser.add_argument("-r", "--readfile", metavar='<filename>', type=str, help="switch to read the specified file")
    parser.add_argument("-s", "--show", action="store_true", help="switch to print files in server")
    parser.add_argument("-k", "--kill", action="store_true", help="switch to kill all instances")
    parser.add_argument("-p", '--prompt', type=str, help='switch to prompt for reverse shell')

    return parser

if __name__ == "__main__":
    arguments()