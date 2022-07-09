import ast
import importlib.util
import inspect
import os
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Optional

from pydantic_lambda_handler.main import PydanticLambdaHandler


def get_top_imported_names(file: str) -> set[str]:
    """Collect names imported in given file.

    We only collect top-level names, i.e. `from foo.bar import baz`
    will only add `foo` to the list.
    """
    if not file.endswith(".pyi"):
        return set()
    with open(os.path.join(file), "rb") as f:
        content = f.read()
    parsed = ast.parse(content)
    top_imported = set()
    for node in ast.walk(parsed):
        if isinstance(node, ast.Import):
            for name in node.names:
                top_imported.add(name.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level > 0:
                # Relative imports always refer to the current package.
                continue
            assert node.module
            top_imported.add(node.module.split(".")[0])
    return top_imported


def gen_open_api_inspect(dir_path: Path):
    files = dir_path.rglob("*.py")

    open_api: dict[str, Any] = {"openapi": "3.0.2"}

    app: Optional[PydanticLambdaHandler] = None

    for file in files:
        module_name = ".".join(str(file.relative_to(dir_path)).removesuffix(".py").split("/"))
        spec = importlib.util.spec_from_file_location(module_name, file)
        if not spec or not spec.loader:
            continue
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        results = inspect.getmembers(module)

        for i in range(0, len(results)):
            if isinstance(results[i][1], PydanticLambdaHandler):
                app = deepcopy(results[i][1])

    if app:
        open_api["paths"] = app.paths
        open_api["info"] = {"title": app.title}

    return open_api
