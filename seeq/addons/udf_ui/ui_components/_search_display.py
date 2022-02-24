import ipyvuetify as v
import traitlets
from typing import Callable
from pathlib import Path
from seeq.addons.udf_ui.backend import return_func_if_callable

CURRENT_DIR = Path(__file__).parent.resolve()


class SearchDisplay(v.VuetifyTemplate):
    """
    """

    template_file = str(CURRENT_DIR.joinpath('templates', 'SearchDisplay.vue'))
    class_functionality = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    search_visible = traitlets.Bool(default_value=True).tag(sync=True)
    package_list = traitlets.List(default_value=[]).tag(sync=True)
    selected_package = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    function_list = traitlets.List(default_value=[]).tag(sync=True)
    selected_function = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)

    def __init__(self, *args,
                 fetch_packages: Callable[[None], str] = None,
                 update_package_object_on_change: Callable[[None], None] = None,
                 update_function_on_change: Callable[[None], None] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.class_functionality = self.set_default('class_functionality', 'UDF Search or Create',
                                                    **kwargs)

        self.fetch_packages = return_func_if_callable(fn=fetch_packages, template_name=self.__class__.__name__)
        self.update_package_object_on_change = return_func_if_callable(fn=update_package_object_on_change,
                                                                       template_name=self.__class__.__name__)
        self.update_function_on_change = return_func_if_callable(fn=update_function_on_change,
                                                                 template_name=self.__class__.__name__)
        self.package_list = self.fetch_packages()

    @staticmethod
    def set_default(arg, default, **kwargs):
        return default if kwargs.get(arg) is None else kwargs.get(arg)

    def vue_update_package_object(self, data=None):
        if data:
            self.selected_package = data
            self.update_package_object_on_change(data)

    def vue_update_function(self, data=None):
        if data:
            self.selected_function = data
            self.update_function_on_change(self.selected_function)

    def on_package_change(self, package_and_functions):
        self.function_list = package_and_functions['function_list']
        self.selected_function = ''

    def on_submit_refresh(self, package=None):
        self.package_list = self.fetch_packages()
        if package:
            self.update_package_object_on_change(package)
