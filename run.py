import argparse
import os


def run_server():
    cmd = 'cd server && python3.10 manage.py runserver 0.0.0.0:8282'
    os.system(cmd)


def run_qcluster():
    cmd = 'cd server && python3.10 manage.py qcluster'
    os.system(cmd)


def run_bot():
    cmd = 'cd client && python3.10 bot.py TimeTableBot'
    os.system(cmd)


def main():
    parser = argparse.ArgumentParser(description='TimeTableBot')
    parser.add_argument('-s', '--server', help='gunicorn',
                        action='store_true')
    parser.add_argument('-q', '--qcluster', help='qcluster',
                        action='store_true')
    parser.add_argument('-b', '--bot', help='test',
                        action='store_true')

    args = parser.parse_args()
    if args.server:
        run_server()

    if args.qcluster:
        run_qcluster()

    if args.bot:
        run_bot()


if __name__ == "__main__":
    main()
