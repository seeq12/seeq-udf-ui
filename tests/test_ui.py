import pytest
from seeq.addons import udf_ui
from seeq.addons.udf_ui import ui_components
from . import test_common

test_common.login()
ui = udf_ui.UserDefinedFunctionsUI()


@pytest.mark.unit
def test_ui_instance():
    # This tests doesn't tests the rendering of the UI, just the instantiation of the UI, and checks whether the
    # 'visible' flag of the appropriate displays are set
    assert isinstance(ui.app, ui_components.AppLayout)
    assert isinstance(ui.app.search_display, ui_components.SearchDisplay)
    assert isinstance(ui.app.summary_page, ui_components.SummaryPage)
    assert isinstance(ui.app.function_documentation, ui_components.FunctionDocumentation)
    assert isinstance(ui.app.access_management, ui_components.AccessManagement)
    assert isinstance(ui.app.function_parameters_display, ui_components.FunctionParametersDisplay)
    assert ui.app.search_display.search_visible
    assert ui.app.summary_page.summary_visible
    assert not ui.app.function_documentation.description_visible
    assert not ui.app.function_parameters_display.parameters_visible


@pytest.mark.unit
def test_ui_components_visible():
    ui.app.search_display.vue_update_package_object(data='testPackage')
    ui.app.search_display.vue_update_function(data='testFunction')
    assert ui.app.function_documentation.description_visible
    assert ui.app.function_parameters_display.parameters_visible

    ui.app.summary_page.vue_on_review(data='')
    assert ui.app.summary_page.summary_visible

