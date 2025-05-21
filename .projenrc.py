import json
from projen.python import PythonProject
from projen.python import PoetryPyprojectOptionsWithoutDeps

from projects.generic_project import GenericPythonProject
from utils import create_readonly_file
from templates.github.workflows.generic.on_publish_main import on_publish_main
from templates.coverage import coverage
from templates.flake8 import flake8
from templates.Makefile import Makefile
from projen import TextFile


options = ""
with open(".projenrc.projdata.json") as options_file:
    options = json.load(options_file)

project = GenericPythonProject(
    author_email=options["email"],
    author_name=options["author"],
    module_name=options["name"],
    name=options["name"],
    version=options["version"],
    projenrc_python=True,
    pip=False,
    venv=False,
    setuptools=False,
    poetry=True,
    github=False,
    deps=["python@^3.11"] + options.get("deps", []),
    dev_deps=[
        "black@*", "flake8@*", "isort@*", "liccheck@*", "mypy@*", "pytest-cov@*"
    ] + options.get("dev_deps", []),
    poetry_options=PoetryPyprojectOptionsWithoutDeps(
        extras=options.get("extras", {}),
        include=options.get("include", []),
        exclude=options.get("exclude", []),
        scripts=options.get("scripts", {}),
        source=options.get("source", []),
        version=options["version"],
    ),
)

project.add_git_ignore(".terraform*")
project.add_git_ignore(".scannerwork*")
project.add_git_ignore(".idea*")

# GitHub Actions & template setup
create_readonly_file(project, ".github/ISSUE_TEMPLATE/new-issue-template.md", "github/ISSUE_TEMPLATE/new-issue-template.md")
create_readonly_file(project, ".github/workflows/on-push.yml", "github/workflows/on-push.yml")

main_branch = options.get("main_branch", "main")
TextFile(project, lines=on_publish_main(options).splitlines(), file_path=f".github/workflows/generic/on-publish-{main_branch}.yml")

create_readonly_file(project, ".darglint")
create_readonly_file(project, "liccheck.ini")
create_readonly_file(project, "mypy.ini")

TextFile(project, lines=coverage(options).splitlines(), file_path=".coveragerc")
TextFile(project, lines=flake8(options).splitlines(), file_path=".flake8")
TextFile(project, lines=Makefile(options).splitlines(), file_path="Makefile")

for entry in sorted(set(options.get("gitignore", []))):
    project.add_git_ignore(entry)

project.synth()
