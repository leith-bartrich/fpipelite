import argparse
import fpipelite.cli.projects
import fpipelite.cli.workspace
import pkg_resources

def main():
    #commands
    parser = argparse.ArgumentParser(prog="fpipelite")
    commands_subparsers = parser.add_subparsers(help='commands')

    #project command
    project_parser = commands_subparsers.add_parser('project')
    project_subparsers = project_parser.add_subparsers(help='project commands')
    fpipelite.cli.projects.print_parser(project_subparsers.add_parser('print'))
    fpipelite.cli.projects.new_parser(project_subparsers.add_parser('new'))
    fpipelite.cli.projects.delete_parser(project_subparsers.add_parser('delete'))
    #plugins
    execute_argparse_plugin('fpipelite.cli.argparse.commands.project', project_subparsers)

    #workspace command
    workspace_parser = commands_subparsers.add_parser('workspace')
    workspace_subparsers = workspace_parser.add_subparsers(help='workspace commands')
    fpipelite.cli.workspace.print_parser(workspace_subparsers.add_parser('print'))
    fpipelite.cli.workspace.new_parser(workspace_subparsers.add_parser('new'))
    fpipelite.cli.workspace.delete_parser(workspace_subparsers.add_parser('delete'))
    #plugins
    execute_argparse_plugin('fpipelite.cli.argparse.commands.workspace', workspace_subparsers)

    #commands plugins
    execute_argparse_plugin('fpipelite.cli.argparse.commands',commands_subparsers)

    #parse and go!
    args:argparse.Namespace = parser.parse_args()
    if "func" in args:
        f = args.func
        f(args)
    else:
        print("No valid command command given.")
        #TODO:  Find a way to at least print help for the given subcommand?
        parser.print_help()

def execute_argparse_plugin(entry_point_name:str, argument):
    entrypoints = pkg_resources.iter_entry_points(entry_point_name)
    for entrypoint in entrypoints:
        #print(self.colorize("Loading shell plugin: " + entrypoint.name + ":" + pluginname, colorama.Fore.GREEN))
        method = entrypoint.load()
        method(argument)


