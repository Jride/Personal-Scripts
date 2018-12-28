import sys
import os
import re

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_SCRIPTS') + "/Xcode")

import itv_shell
import itv_git
import itv_argparser
import OpenXcodeProject

def get_branch_name():
    print("Enter your branch name: ")
    return input()

def get_ticket_number():
    print("Enter the JIRA ticket number: ")
    return input()

def get_feature_name():
    print("Enter the name of the feature: ")
    return input()

def checkout_and_open(branch_name):
    itv_shell.run("git checkout %s" % branch_name)
    print("Opening Xcode...")
    OpenXcodeProject.run()

def validate_branch_name(branch_name):
    pass_naming_validation = False
    while pass_naming_validation == False:
        branch_name = branch_name.replace(" ", "-")
        pattern = re.compile(r"^((IPIA|TVOS)-(0|[1-9][0-9]*))")
        result = pattern.match(branch_name)
        if result:
            pass_naming_validation = True
        else:
            print("")
            print("A feature branch name should start with the format:")
            print("IPIA-{ticket_number} or TVOS-{ticket_number}")
            print("")
            branch_name = get_branch_name()

    return branch_name

### --- MAIN --- ###
def run(args):

    # Parse the arguments
    parser = itv_argparser.parser(
    os.path.dirname(__file__),
    '''
    Creates a new feature branch with the correct naming conventions
    '''
    )
    parser.add_argument('--branchname', help='''
    The branch name. By providing this it will bypass the need to
    input the ticket number or feature name
    ''')
    parser.add_argument('--featurename', help='The name of the feature you are working on')
    parser.add_argument('--ticketnumber', help='The JIRA ticket number related to the feature', type=int)
    args = parser.parse_args(args)

    if itv_git.is_git_repo() == False:
        print("Current directory is not a git repository")
        sys.exit()

    if itv_git.is_working_copy_clean() == False:
        print("Working copy isn't clean. Commit or remove any changed files")
        sys.exit()

    # If the branch was provided then validate it
    if args.branchname:
        branch_name = validate_branch_name(args.branchname)
    else:
        # Else we need to complile the name from the ticket number and feature name
        if itv_git.is_ios_repo():
            project = "IPIA"
        elif itv_git.is_tvos_repo():
            project = "TVOS"
        else:
            project = "IPIA" if itv_shell.yes_or_no_input("Is this for the ios project?") else "TVOS"

        ticket_number = args.ticketnumber if args.ticketnumber else get_ticket_number()
        feature_name = args.featurename if args.featurename else get_feature_name()

        branch_name = project + "-" + ticket_number + "-" + feature_name
        branch_name = validate_branch_name(branch_name)

    branch_name = "feature/%s" % branch_name

    # Check to see if there already is a branch with that name
    if itv_git.does_local_branch_exist(branch_name):
        print("Branch already exists")
        print("Checking out branch...")
        checkout_and_open(branch_name)
        sys.exit()

    itv_shell.run("git branch %s" % branch_name)
    checkout_and_open(branch_name)

if __name__ == "__main__":
    arguments = sys.argv[1:]
    run(arguments)
