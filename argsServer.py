import argparse


"""
fonction qui permet de parser les arguments passés en ligne de commande
"""
def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--listen", metavar='<port>', type=int, help="switch to listen on specified port")
    parser.add_argument("-r", "--readfile", metavar='<filename>', type=str, help="switch to read the specified file")
    parser.add_argument("-s", "--show", action="store_true", help="switch to print files in server")
    parser.add_argument("-k", "--kill", action="store_true", help="switch to kill all instances")
    parser.add_argument("-t","--target",action="store_true",help="switch to list all target")
    parser.add_argument("-v","--victim",metavar='<victim>',type=str,help="switch to specify id of victim for reverse shell")
    return parser.parse_args()


if __name__ == "__main__":
    arguments()