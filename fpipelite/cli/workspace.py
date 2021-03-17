import os
import sys
import argparse
import pathlib
import fpipelite.data.workspace
import fpipelite.data.data
import json


def print_parser(parser: argparse.ArgumentParser):
    parser.add_argument("path", type=pathlib.Path, nargs="?", default=".")
    parser.description = "Prints the data for a found workspace via {path}."
    parser.set_defaults(func=print_exec)


def print_exec(args: argparse.Namespace):
    found, data = fpipelite.data.workspace.FindWorkspaceFromPath(os.path.abspath(str(args.path)))

    if not found:
        exit(-1)

    else:
        print(json.dumps(data.json_data, indent=4, sort_keys=True))
        exit()


def new_parser(parser: argparse.ArgumentParser):
    parser.description = "Creates a new workspace with the given data, at {dir}."
    # parser.add_argument("--short",required=True, type=str, help="The short name of the project.")
    # parser.add_argument("--long",required=True, type=str, help="The long name of the project.")
    parser.add_argument("dir", type=pathlib.Path, nargs="?", default=".",
                        help="The directory to put the workspace in.  Current directory if omitted.")
    parser.set_defaults(func=new_exec)


def new_exec(args: argparse.Namespace):
    dir = os.path.join(os.path.abspath(args.dir), fpipelite.data.data._FPipeLiteDirName)
    os.makedirs(dir,exist_ok=True)
    fname = os.path.join(dir, fpipelite.data.data.FPipeLiteDataFilenameFromType("workspace"))

    data = fpipelite.data.workspace.NewWorkspace(fname)
    data.save()


def delete_parser(parser: argparse.ArgumentParser):
    parser.description = "Deletes a workspace's data at the {dir}"
    parser.add_argument("-f", help="Forces the deletion without asking for confirmation.")
    parser.add_argument("path", type=pathlib.Path, nargs="?", default=".",
                        help="The path to search from.  defaults to '.' if not specified.")
    parser.set_defaults(func=delete_exec)


def delete_exec(args: argparse.Namespace):
    found, data = fpipelite.data.workspace.FindWorkspaceFromPath(os.path.abspath(str(args.path)))
    if not found:
        print("No workspace found at path: " + os.path.abspath(str(args.path)))
        exit(-1)
    dir = data.get_fpipelite_dir_path()
    path = os.path.join(dir, fpipelite.data.data.FPipeLiteDataFilenameFromType("workspace"))
    if not os.path.exists(path):
        print("The workspace file path does not exist: " + path)
        exit(-1)
    if not os.path.isfile(path):
        print("The workspace file path does not point to a file: " + path)
        exit(-1)

    if not args.f:
        # f is not specified.
        answer = input("Are you sure? (y/n): ")
        if answer.lower() != "y":
            print("canceling deletion.")
            exit()

    os.unlink(path)
    exit()
