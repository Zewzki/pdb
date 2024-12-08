from pathlib import Path
from pdb.app.client.rendering.renderer import Renderer
from typing import Any

from jinja2 import Environment


class JinjaRenderer(Renderer):
    def __init__(self, env: Environment) -> None:
        self._env = env

    def render(self, template_path: Path, context: dict[str, Any]) -> str:
        try:
            template = self._env.get_template(template_path.as_posix())
            return template.render(context)
        except Exception as ex:
            raise ex from ex
