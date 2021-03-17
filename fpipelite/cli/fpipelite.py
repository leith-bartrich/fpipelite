import argparse
import fpipelite.cli.projects
import fpipelite.cli.workspace

def main():
    parser = argparse.ArgumentParser(prog="fpipelite")
    subparsers = parser.add_subparsers(help='commands')

    #project
    project_parser = subparsers.add_parser('project')
    project_subparsers = project_parser.add_subparsers(help='project commands')
    fpipelite.cli.projects.print_parser(project_subparsers.add_parser('print'))
    fpipelite.cli.projects.new_parser(project_subparsers.add_parser('new'))
    fpipelite.cli.projects.delete_parser(project_subparsers.add_parser('delete'))

    #workspace
    workspace_parser = subparsers.add_parser('workspace')
    workspace_subparsers = workspace_parser.add_subparsers(help='workspace commands')
    fpipelite.cli.workspace.print_parser(workspace_subparsers.add_parser('print'))
    fpipelite.cli.workspace.new_parser(workspace_subparsers.add_parser('new'))
    fpipelite.cli.workspace.delete_parser(workspace_subparsers.add_parser('delete'))

    #parse and go!
    args:argparse.Namespace = parser.parse_args()
    if "func" in args:
        f = args.func
        f(args)
    else:
        print("No valid command command given.")
        #TODO:  Find a way to at least print help for the given subcommand?
        parser.print_help()
