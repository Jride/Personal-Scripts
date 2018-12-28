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
    Creates a tag from the current branch with the provided name
    and pushes it to the repository
    '''
    )
    parser.add_argument('tagname', help='The name of the tag')
    args = parser.parse_args(args)

    tag_name = args.tagname

    # Deletes any tag that might exist with the same name
    remote_tag = itv_shell.result('git tag -l %s' % tag_name)
    if remote_tag == tag_name:
        print("The tag (%s) already exists, deleting..." % tag_name)
        itv_shell.run('git push --delete origin %s' % tag_name)
        itv_shell.run('git tag -d %s' % tag_name)

    itv_shell.run('git tag %s' % tag_name)
    itv_shell.run('git push origin %s' % tag_name)
    print('Successfully created tag: %s' % tag_name)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    run(arguments)
