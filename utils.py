from projen import TextFile


def create_readonly_file(project, file_path, template_path="", readonly=True):
    """Create a projen-managed file at the specified file path from the specified template

    Params:
        project: The project in which to create the file
        file_path: The file path within the project at which to create the file
        template path: The relative path to the template within the templates directory
    """
    if template_path == "":
        template_path = file_path

    file = open(f"projen-cmdline-tool-submodule/templates/{template_path}", "r")
    lines = file.read().splitlines()
    TextFile(scope=project, lines=lines, readonly=readonly, file_path=file_path)
