import ipyvuetify as v
import traitlets
from typing import Callable
from pathlib import Path
from seeq.addons.udf_ui.backend import return_func_if_callable

CURRENT_DIR = Path(__file__).parent.resolve()


class FunctionParametersDisplay(v.VuetifyTemplate):
    """
    """

    template_file = str(CURRENT_DIR.joinpath('templates', 'FunctionParametersDisplay.vue'))
    class_functionality = traitlets.Unicode(allow_none=True, default_value='Inputs and Formula').tag(sync=True)
    params_and_types = traitlets.List(default_value=[]).tag(sync=True)
    params_options = traitlets.List(default_value=['Signal', 'Scalar', 'Condition']).tag(sync=True)
    adding_in_progress = traitlets.Bool(default_value=False).tag(sync=True)
    deleting_in_progress = traitlets.Bool(default_value=False).tag(sync=True)
    add_active = traitlets.Bool(default_value=True).tag(sync=True)
    delete_active = traitlets.Bool(default_value=True).tag(sync=True)
    avail_active = traitlets.Bool(default_value=True).tag(sync=True)
    parameters_visible = traitlets.Bool(default_value=False).tag(sync=True)
    formula = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    param_name = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    input_type = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    parse_dialog_open = traitlets.Bool(default_value=False).tag(sync=True)

    def __init__(self, *args, parse_params: Callable[[None], list] = None,
                 update_params_formula_on_request: Callable[[None], list] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.parse_params = return_func_if_callable(fn=parse_params, template_name=self.__class__.__name__)
        self.update_params_formula_on_request = return_func_if_callable(fn=update_params_formula_on_request,
                                                                        template_name=self.__class__.__name__)

    @staticmethod
    def set_default(arg, default, **kwargs):
        return default if kwargs.get(arg) is None else kwargs.get(arg)

    def vue_add_param(self, data):
        temp_list = self.params_and_types
        temp_list.append({'name': '', 'type': ''})

        self.params_and_types = []
        self.params_and_types = temp_list

    def vue_delete_param(self, data):
        index = data

        temp_list = self.params_and_types
        del temp_list[index]

        self.params_and_types = []
        self.params_and_types = temp_list

    def vue_update_param(self, data=None):
        selection = data[0]
        index = data[1]
        param_attribute = data[2]
        temp_list = self.params_and_types
        temp_list[index][param_attribute] = selection
        self.params_and_types = []
        self.params_and_types = temp_list

    def vue_use_param_in_formula(self, data=None):
        index = data
        self.formula = self.formula + ' $' + self.params_and_types[index]['name']

    def vue_parse_on_click(self, data=None):
        self.params_and_types = []
        self.params_and_types = self.parse_params(self.formula)

    def vue_on_clear_formula(self, data):
        self.formula = ''

    def on_function_change(self, function_and_switches):
        self.parameters_visible = function_and_switches['display_switches'].parameters_visible
        if not function_and_switches['function'].func_is_new:
            self.params_and_types = function_and_switches['function'].parameters
            self.formula = function_and_switches['function'].formula

    def on_update_request(self, update_requested):
        if update_requested:
            self.update_params_formula_on_request({'params_and_types': self.params_and_types, 'formula': self.formula})
