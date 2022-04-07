import ipyvuetify as v
import traitlets
from typing import Callable
from pathlib import Path
from seeq.addons.udf_ui.backend import return_func_if_callable

CURRENT_DIR = Path(__file__).parent.resolve()


class SummaryPage(v.VuetifyTemplate):
    """
    """

    template_file = str(CURRENT_DIR.joinpath('templates', 'SummaryPage.vue'))
    class_functionality = traitlets.Unicode(allow_none=True, default_value='Review and Submit').tag(sync=True)
    summary_visible = traitlets.Bool(default_value=True).tag(sync=True)
    summary_open = traitlets.Bool(default_value=False).tag(sync=True)
    delete_open = traitlets.Bool(default_value=False).tag(sync=True)
    selected_package = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    selected_function = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    params_and_types = traitlets.List(default_value=[]).tag(sync=True)
    formula = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    func_description = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    package_description = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    examples_and_descriptions = traitlets.List(default_value=[]).tag(sync=True)
    selected_users_dict = traitlets.List(allow_none=True, default_value=[]).tag(sync=True)
    package_is_new = traitlets.Bool(default_value=False).tag(sync=False)
    func_is_new = traitlets.Bool(default_value=False).tag(sync=False)
    action = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    delete_choices = traitlets.List(default_value=['Function', 'Package']).tag(sync=True)
    selected_for_delete = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)

    def __init__(self, *args,
                 request_updated_summary_on_review: Callable[[None], str] = None,
                 submit_changes: Callable[[None], str] = None,
                 archive_object: Callable[[None], str] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.submit_changes = return_func_if_callable(fn=submit_changes, template_name=self.__class__.__name__)
        self.archive_object = return_func_if_callable(fn=archive_object, template_name=self.__class__.__name__)
        self.request_updated_summary_on_review = return_func_if_callable(fn=request_updated_summary_on_review, template_name=self.__class__.__name__)

    def vue_on_review(self, data):
        if self.package_is_new:
            self.action = 'Create new package and function'
        elif self.func_is_new:
            self.action = 'Add new function to existing package'
        elif self.selected_function:
            self.action = 'Modify existing function'
        self.request_updated_summary_on_review()

    def vue_on_submit(self, data):
        self.submit_changes()

    def vue_on_delete(self, data):
        self.archive_object(self.selected_for_delete)

    def vue_update_delete_choices(self, data):
        self.delete_choices = []
        if self.package_is_new or not self.selected_package:
            pass
        elif self.func_is_new or not self.selected_function:
            self.delete_choices = ['Package: ' + self.selected_package]
        else:
            self.delete_choices = ['Function: ' + self.selected_function, 'Package: ' + self.selected_package]

    def on_package_change(self, package_and_functions):
        self.package_is_new = package_and_functions['package'].is_new_package
        self.selected_package = package_and_functions['package'].name
        self.selected_function = ''

    def on_function_change(self, function_and_display_switches):
        self.selected_function = function_and_display_switches['function'].name
        self.func_is_new = function_and_display_switches['function'].func_is_new

    def on_update_summary(self, summary):
        self.selected_function = ''
        self.params_and_types = []
        self.formula = ''
        self.func_description = ''
        self.package_description = ''
        self.examples_and_descriptions = []
        self.selected_users_dict = []
        self.func_is_new = summary['function'].func_is_new
        self.selected_function = summary['function'].name
        self.params_and_types = summary['params_and_types']
        self.formula = summary['formula']
        self.func_description = summary['function_description']
        self.package_description = summary['package_description']
        self.examples_and_descriptions = summary['examples_and_descriptions']
        self.selected_users_dict = summary['users_dict']



