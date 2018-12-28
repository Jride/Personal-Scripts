import sys
import os

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))

import itv_shell
import itv_argparser

### --- MAIN --- ###
def run(args = []):

    # Parse the arguments
    parser = itv_argparser.parser(
    os.path.dirname(__file__),
    '''Opens the provided file in the TextEdit application'''
    )
    parser.add_argument('file', help='Path to the file to open')
    args = parser.parse_args(args)

    itv_shell.run('open -a TextEdit "%s"' % args.file)

if __name__ == "__main__":
    arguments = sys.argv[1:]
    run(arguments)
