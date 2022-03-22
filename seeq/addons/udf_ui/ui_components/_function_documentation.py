import ipyvuetify as v
import traitlets
from pathlib import Path
from typing import Callable
from seeq.addons.udf_ui.backend import return_func_if_callable, debounce_with_timer
from markdown import markdown as markdown_to_html
from unmarkd import unmark as html_to_markdown

CURRENT_DIR = Path(__file__).parent.resolve()


class FunctionDocumentation(v.VuetifyTemplate):
    """
    """

    template_file = str(CURRENT_DIR.joinpath('templates', 'FunctionDocumentation.vue'))
    class_functionality = traitlets.Unicode(allow_none=True, default_value='UDF Documentation').tag(sync=True)
    description_visible = traitlets.Bool(default_value=False).tag(sync=True)
    examples_visible = traitlets.Bool(default_value=False).tag(sync=True)
    function_updated = traitlets.Bool(default_value=False).tag(sync=True)
    examples_and_descriptions = traitlets.List(default_value=[]).tag(sync=True)
    add_example_active = traitlets.Bool(default_value=True).tag(sync=True)
    example_added = traitlets.Bool(default_value=False).tag(sync=True)
    examples_editor_open = traitlets.Bool(default_value=False).tag(sync=True)
    access_management_open = traitlets.Bool(default_value=False).tag(sync=True)
    func_description_html = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    package_description_html = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    func_description_markdown = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    package_description_markdown = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    func_description_toggle = traitlets.Integer(default_value=0, allow_none=True).tag(sync=True)
    package_description_toggle = traitlets.Integer(default_value=0, allow_none=True).tag(sync=True)

    def __init__(self, *args, update_doc_on_request: Callable[[None], list] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.update_doc_on_request = return_func_if_callable(fn=update_doc_on_request,
                                                             template_name=self.__class__.__name__)

    @staticmethod
    def set_default(arg, default, **kwargs):
        return default if kwargs.get(arg) is None else kwargs.get(arg)

    def vue_add_example(self, data):
        temp_list = self.examples_and_descriptions
        temp_list.append({'description': '', 'formula': ''})

        self.examples_and_descriptions = []
        self.examples_and_descriptions = temp_list

    def vue_delete_example(self, data):
        index = data
        temp_list = self.examples_and_descriptions
        del temp_list[index]
        self.examples_and_descriptions = []
        self.examples_and_descriptions = temp_list

    @debounce_with_timer(wait_time=0.3)
    def vue_update_func_desc_html(self, data):
        self.func_description_html = markdown_to_html(self.func_description_markdown)

    @debounce_with_timer(wait_time=0.3)
    def vue_update_package_desc_html(self, data):
        self.package_description_html = markdown_to_html(self.package_description_markdown)

    @debounce_with_timer(wait_time=0.3)
    def vue_update_func_desc_markdown(self, data):
        self.func_description_markdown = html_to_markdown(self.func_description_html)

    @debounce_with_timer(wait_time=0.3)
    def vue_update_package_desc_markdown(self, data):
        self.package_description_markdown = html_to_markdown(self.package_description_html)

    def on_function_change(self, function_and_switches):
        self.function_updated = function_and_switches['function'].function_updated
        self.examples_and_descriptions = function_and_switches['function'].examples_and_descriptions
        self.description_visible = function_and_switches['display_switches'].description_visible
        self.examples_visible = function_and_switches['display_switches'].examples_visible

        if not function_and_switches['function'].func_is_new:
            self.func_description_html = function_and_switches['function'].description
            self.func_description_markdown = html_to_markdown(self.func_description_html)

    def on_package_change(self, package_and_functions):
        if package_and_functions['package'].description:
            self.package_description_html = package_and_functions['package'].description
            self.package_description_markdown = html_to_markdown(self.package_description_html)

    def on_update_request(self, update_requested):
        if update_requested:
            self.update_doc_on_request({'package_description': self.package_description_html,
                                        'function_description': self.func_description_html,
                                        'examples_and_descriptions': self.examples_and_descriptions})
