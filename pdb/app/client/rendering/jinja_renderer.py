from pdb.app.client.rendering.renderer import Renderer
from pdb.shared.op_status import OpStatus
from typing import Any

from jinja2 import Environment, Template, TemplateNotFound


class JinjaRenderer(Renderer):
    def __init__(self, env: Environment) -> None:
        self._env = env

    def render(self, template: str, context: dict[str, Any] = {}) -> OpStatus:
        try:
            template: Template = self._env.get_template(template)
        except TemplateNotFound as tnf:
            return OpStatus(False, f"Template {template} not found...")

        try:
            content = template.render(context)
            return OpStatus(True, content)
        except Exception as ex:
            return OpStatus(False, f"Error rendering template {template} - {ex}")
