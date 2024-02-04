import argsServer
import server
import sys

def main():
    try:
        option = ""
        listports = []

        while option not in ["-k", "--kill"]:
            option = input("Choose your flag: ")

            if option in ["-h", "--help"]:
                argsServer.arguments()
            elif "-l" in option or "--listen" in option:
                listports.append(server.listen(option))
            elif "-r" in option or "--readfile" in option:
                server.readfile(option)
            elif "-s" in option or "--show" in option:
                server.show()
            elif option in ["-k", "--kill"]:
                sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)