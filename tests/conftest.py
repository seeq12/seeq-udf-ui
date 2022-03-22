import pytest
from seeq.addons import udf_ui
from . import test_common
from seeq import spy


@pytest.fixture(scope='session', autouse=True)
def user_login_and_setup():
    test_common.login()
    if not spy.user.is_admin:
        pytest.skip(f'The UDF Editor tests are skipped for non-admin users as the tests depend on '
                    f'the user\'s ability to permanently delete UDFs')
    test_common.admin_clean_up(['testPackage', 'testPackageAccessControl'])


@pytest.fixture
def instantiate_ui_create_function_and_package():
    def function_and_package(package_name, function_name):
        ui = udf_ui.UserDefinedFunctionsUI()
        ui.app.search_display.vue_update_package_object(data=package_name)
        ui.app.search_display.vue_update_function(data=function_name)

        ui.app.function_parameters_display.params_and_types = [{'name': 'a', 'type': 'Signal'},
                                                               {'name': 'b', 'type': 'Signal'}]
        ui.app.function_parameters_display.formula = '$a + $b'
        ui.app.function_documentation.package_description_html = '<p>Test package</p>'
        ui.app.function_documentation.func_description_html = '<p>Test function</p>'

        ui.app.access_management.selected_users_dict = [{'name': spy.user.name,
                                                         'username': spy.user.username,
                                                         'type': 'User',
                                                         'read': True,
                                                         'write': True,
                                                         'manage': True},
                                                        {'name': 'Everyone',
                                                         'username': None,
                                                         'type': 'UserGroup',
                                                         'read': True,
                                                         'write': False,
                                                         'manage': False}
                                                        ]
        ui.app.summary_page.vue_on_review(data='')
        ui.app.summary_page.vue_on_submit(data='')

        # By default the UI unselects the function after submit to avoid accidental editing of the same function
        # we reselect it for the tests:
        ui.app.search_display.vue_update_function(data=function_name)

        return ui

    yield function_and_package
    test_common.admin_clean_up(['testPackage', 'testPackageAccessControl'])
