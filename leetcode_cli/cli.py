import os
import sys
import argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from leetcode_cli.detail import detail
from leetcode_cli.list import list_question
from leetcode_cli.stat import stat
from leetcode_cli.today import today
from leetcode_cli.session import build_session
from leetcode_cli.config import Config
from leetcode_cli.submit import test
from leetcode_cli.submit import submit


session = build_session()


def main():
    parser = argparse.ArgumentParser(
            prog = 'LeetCode',
            description="LeetCode in command line"
    )

    subparser = parser.add_subparsers(title='Command Options', dest='cmd')
    
    show_parser = subparser.add_parser(name='show')
    show_parser.add_argument("--question", required=False)

    list_parser = subparser.add_parser(name='list')
    list_parser.add_argument("--level", type=str)
    list_parser.add_argument("--undo", type=bool, default=False)
    list_parser.add_argument("--free", type=bool, default=False)

    stat_parser = subparser.add_parser(name='stat')
    today_parser = subparser.add_parser(name='today')
    
    test_parser = subparser.add_parser(name='test')
    test_parser.add_argument("--file", type=str)

    submit_parser = subparser.add_parser(name='submit')
    submit_parser.add_argument("--file", type=str)
    
    args = parser.parse_args()
    
    cmd = vars(args)['cmd']
    if cmd == 'show':
        question = args.question
        detail(question=question, session=session)
    elif cmd == 'list':
        level = args.level
        undo = args.undo
        free = args.free
        questions = list_question(level=level, undo=undo, free=free, session=session)
    elif cmd == 'stat':
        stat(session=session)
    elif cmd == 'today':
        today(session=session)
    elif cmd == 'test':
        file = args.file
        test(file=file, session=session)
    elif cmd == 'submit':
        file = args.file
        submit(file=file, session=session)

if __name__ == "__main__":
    main()
