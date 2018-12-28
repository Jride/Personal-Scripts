import sys
import os

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))

import itv_shell
import itv_argparser

### --- MAIN --- ###
def run(args):

    # Parse the arguments
    parser = itv_argparser.parser(
    os.path.dirname(__file__),
    '''
    Deletes all local branches that have been merged into the current branch
    '''
    )
    args = parser.parse_args(args)

    itv_shell.run('git branch --merged | egrep -v "(^\*|master|dev|develop|development|release)" | xargs git branch -d')

if __name__ == "__main__":
    arguments = sys.argv[1:]
    run(arguments)
