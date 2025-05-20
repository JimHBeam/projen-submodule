import os
import stat
from projen.python import PythonProject, PoetryPyprojectOptionsWithoutDeps
from projen import TextFile
from templates.sonar import sonar


class GenericPythonProject(PythonProject):
    def __init__(
        self,
        *,
        author_name,
        author_email,
        module_name,
        name,
        version,
        deps=None,
        dev_deps=None,
        pip=None,
        poetry=None,
        projenrc_python=None,
        setuptools=None,
        venv=None,
        github=None,
        poetry_options=None,
    ) -> None:
        super().__init__(
            author_email=author_email,
            author_name=author_name,
            poetry_options=poetry_options,
            module_name=module_name,
            name=name,
            version=version,
            deps=deps,
            dev_deps=dev_deps,
            pip=pip,
            poetry=poetry,
            projenrc_python=projenrc_python,
            venv=venv,
            setuptools=setuptools,
            github=github,
        )

    def post_synthesize(self) -> None:
        # Clean up pyproject.toml (remove single quotes for certain formats)
        with open("pyproject.toml", "r") as file:
            pyproj = file.read()
        pyproj = pyproj.replace("'", "")
        os.chmod("pyproject.toml", stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        with open("pyproject.toml", "w") as file:
            file.write(pyproj)

        # No private registry config
        super().post_synthesize()
