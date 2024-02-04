import argsServer
import server
import sys

def main():
    try:
        option = ""

        while option not in ["-k", "--kill"]:
            option = input("Choisissez votre option: ")

            if option in ["-h", "--help"]:
                argsServer.arguments()
            elif "-l" in option or "--listen" in option:
                server.listen(option)
            elif "-r" in option or "--readfile" in option:
                filename = option.split()[1]
                server.readfile(filename)
            elif "-s" in option or "--show" in option:
                server.show()
            elif option in ["-k", "--kill"]:
                server.kill_all_servers()
    except KeyboardInterrupt:
        server.kill_all_servers()

if __name__ == "__main__":
    main()
