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
    '''Opens Source Tree application from the path provided or
    from the current working directory'''
    )
    parser.add_argument('-p','--path', help='Opens source tree from the given path')
    args = parser.parse_args(args)

    if args.path:
        itv_shell.run('open -a SourceTree "%s"' % args.path)
    else:
        itv_shell.run('open -a SourceTree "."')

if __name__ == "__main__":
    arguments = sys.argv[1:]
    run(arguments)
