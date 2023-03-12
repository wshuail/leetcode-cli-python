import os
import sys
import argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from leetcode_cli.models.session import build_session
from leetcode_cli.models.detail import detail
from leetcode_cli.models.list import list_question
from leetcode_cli.models.stat import stat
from leetcode_cli.models.today import today
from leetcode_cli.models.submit import submit
from leetcode_cli.models.code import code
from leetcode_cli.util import Config
from leetcode_cli.util import init


@init
def main():


    session = build_session()
    
    parser = argparse.ArgumentParser(
            prog = 'LeetCode',
            description="LeetCode in command line"
    )

    subparser = parser.add_subparsers(title='Command Options', dest='cmd')
    
    stat_parser = subparser.add_parser(name='stat', description="show your leetcode stat")
    
    today_parser = subparser.add_parser(name='today', description="show today's question")
    
    list_parser = subparser.add_parser(name='list', description="list questions")
    list_parser.add_argument("--level", "-l", type=str, choices=['easy', 'medium', 'hard'], help="the level of difficulty ['easy', 'medium', 'hard']")
    list_parser.add_argument("--undo", "-u", action="store_true", help="only show undo questions")
    list_parser.add_argument("--free", "-f", action="store_true", help="only show free questions")
    
    show_parser = subparser.add_parser(name='show', description="show the content of a question")
    show_parser.add_argument("question", required=True)
    
    code_parser = subparser.add_parser(name='code', description="download the code template to local")
    code_parser.add_argument("question", required=True)
    code_parser.add_argument("--lang", type=str)

    test_parser = subparser.add_parser(name='test', description="test your code with official cases")
    test_parser.add_argument("file", required=True, type=str)

    submit_parser = subparser.add_parser(name='submit', description="submit your code")
    submit_parser.add_argument("file", required=True, type=str)
    
    args = parser.parse_args()
    
    cmd = vars(args)['cmd']
    if cmd == 'stat':
        stat(session=session)
    elif cmd == 'today':
        today(session=session)
    elif cmd == 'list':
        level = args.level
        undo = args.undo
        free = args.free
        questions = list_question(level=level, undo=undo, free=free, session=session)
    elif cmd == 'show':
        question = args.question
        detail(question=question, session=session)
    elif cmd == 'code':
        question = args.question
        lang = args.lang
        code(question, session, lang)
    elif cmd == 'test':
        file = args.file
        test(file=file, session=session)
    elif cmd == 'submit':
        file = args.file
        submit(file=file, session=session)
    else:
        raise ValueError ('Invalid Argument')

if __name__ == "__main__":
    main()




