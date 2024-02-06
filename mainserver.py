import argsServer
import server
import argsServer

def main():
    try:
        args = argsServer.arguments()

        if args.listen:
            server.listen(args.listen)
        elif args.readfile:
            server.readfile(args.readfile)
        elif args.show:
            server.show()
        elif args.kill:
            server.kill_all_servers()

    except KeyboardInterrupt:
        server.kill_all_servers()

if __name__ == "__main__":
    main()
