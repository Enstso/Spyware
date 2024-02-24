import argsServer
import server
import argsServer
import os
def main():
    try:
        args = argsServer.arguments()

        if args.listen:
            if os.path.exists("kill.txt"):
                os.remove("kill.txt")
            if os.path.exists("serverpid.txt"):
                os.remove("serverpid.txt")
            if os.path.exists("socket.txt"):
                os.remove("socket.txt")

            server.listen(args.listen)
        elif args.readfile:
            server.readfile(args.readfile)
        elif args.show:
            server.show()
        elif args.kill:
            server.kill_all_servers()
        elif args.target:
            server.list_target()
        elif args.victim:
            server.reverse_shell(args.victim)

    except KeyboardInterrupt:
        server.kill_all_servers()

if __name__ == "__main__":
    main()
