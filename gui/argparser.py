from argparse import ArgumentParser


class AP:
    def __init__(self):
        self.parser = ArgumentParser(description='Track flights in real time',
                                     epilog='Author: Alexandr Bagirov')
        self.parser.add_argument('--lat', help='initial map latitude',
                                 default=None)
        self.parser.add_argument('--lon', help='initial map longitude',
                                 default=None)

    def parse(self):
        args, unknown = self.parser.parse_known_args()
        return (args.lat, args.lon) if args.lat and args.lon else None
