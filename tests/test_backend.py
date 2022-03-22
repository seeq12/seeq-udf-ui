from seeq import spy
import pytest
import time


@pytest.mark.system
class TestCreate:
    def test_create_package_and_function(self, instantiate_ui_create_function_and_package):
        ui = instantiate_ui_create_function_and_package('testPackage', 'testFunction')
        assert 'testPackage' in ui.backend.fetch_udf_packages()
        assert 'testPackage' in ui.app.search_display.package_list
        assert 'testFunction' in [func_name.name for func_name in ui.backend.selected_package.package.functions]
        assert 'testFunction' + '($Signal, $Signal)' in ui.app.search_display.function_list

    def test_create_function_same_name(self, instantiate_ui_create_function_and_package):
        ui = instantiate_ui_create_function_and_package('testPackage', 'testFunction')

        ui.app.function_parameters_display.params_and_types = [{'name': 'a', 'type': 'Signal'},
                                                               {'name': 'b', 'type': 'Signal'},
                                                               {'name': 'c', 'type': 'Scalar'}]
        ui.app.function_parameters_display.formula = '$a + $b * $c'
        ui.app.function_documentation.func_description = '<p>Test function with the same name</p>'
        ui.app.function_documentation.examples_and_descriptions = [
            {'description': 'Example 1', 'formula': '$a + $b * $c'},
            {'description': 'Example 2', 'formula': '$c + $d * $e'}]

        ui.app.summary_page.vue_on_review(data='')
        ui.app.summary_page.vue_on_submit(data='')

        assert 'testFunction' + '($Signal, $Signal)' in ui.app.search_display.function_list
        assert 'testFunction' + '($Signal, $Signal, $Scalar)' in ui.app.search_display.function_list


@pytest.mark.system
class TestModify:
    def test_modify_formula(self, instantiate_ui_create_function_and_package):
        ui = instantiate_ui_create_function_and_package('testPackage', 'testFunction')

        ui.app.function_parameters_display.params_and_types = [{'name': 'a', 'type': 'Signal'},
                                                               {'name': 'newParam', 'type': 'Scalar'}]
        ui.app.function_parameters_display.formula = '$a * $newParam'

        ui.app.summary_page.vue_on_review(data='')
        ui.app.summary_page.vue_on_submit(data='')

        ui.app.search_display.vue_update_package_object(data='testPackage')
        ui.app.search_display.vue_update_function(data='testFunction' + '($Signal, $Scalar)')

        assert '$newParam' in ui.app.function_parameters_display.formula
        assert '$newParam' in ui.backend.selected_function.formula

    def test_description(self, instantiate_ui_create_function_and_package):
        ui = instantiate_ui_create_function_and_package('testPackage', 'testFunction')

        ui.app.function_documentation.description_markdown = '## Test Description'
        ui.app.function_documentation.vue_update_html(data='')

        # The markdown-to-html converter has a delay
        time.sleep(0.5)

        assert '<h2>Test Description</h2>' in ui.app.function_documentation.func_description

        ui.app.summary_page.vue_on_review(data='')
        ui.app.summary_page.vue_on_submit(data='')

        ui.app.search_display.vue_update_package_object(data='testPackage')
        ui.app.search_display.vue_update_function(data='testFunction($Signal, $Signal)')

        assert '<h2>Test Description</h2>' in ui.backend.selected_function.func_description

    def test_add_examples(self, instantiate_ui_create_function_and_package):
        ui = instantiate_ui_create_function_and_package('testPackage', 'testFunction')

        examples = [{'description': 'Example 1', 'formula': '$a + $b'},
                    {'description': 'Example 2', 'formula': '$c + $d'}]
        ui.app.function_documentation.examples_and_descriptions = examples

        ui.app.summary_page.vue_on_review(data='')
        ui.app.summary_page.vue_on_submit(data='')

        ui.app.search_display.vue_update_package_object(data='testPackage')
        ui.app.search_display.vue_update_function(data='testFunction($Signal, $Signal)')

        assert ui.backend.selected_function.examples_and_descriptions == examples
        assert ui.app.function_documentation.examples_and_descriptions == examples

    def test_access_control(self, instantiate_ui_create_function_and_package):
        ui = instantiate_ui_create_function_and_package('testPackageAccessControl', 'testFunction')

        ui.app.function_parameters_display.params_and_types = [{'name': 'a', 'type': 'Signal'},
                                                               {'name': 'b', 'type': 'Signal'}]
        ui.app.function_parameters_display.formula = '$a + $b'
        ui.app.function_documentation.func_description = '<p>Test function</p>'

        access_input = [{'name': spy.user.name,
                         'username': spy.user.username,
                         'type': 'User',
                         'read': True,
                         'write': True,
                         'manage': True},
                        {'name': 'Everyone',
                         'username': None,
                         'type': 'UserGroup',
                         'read': True,
                         'write': True,
                         'manage': True}
                        ]

        ui.app.access_management.selected_users_dict = access_input
        ui.app.summary_page.vue_on_review(data='')
        ui.app.summary_page.vue_on_submit(data='')

        ui.app.search_display.vue_update_package_object(data='testPackageAccessControl')

        assert access_input[0] in ui.backend.selected_package.permissions
        assert access_input[1] in ui.backend.selected_package.permissions


@pytest.mark.system
class TestDelete:
    def test_archive_function(self, instantiate_ui_create_function_and_package):
        ui = instantiate_ui_create_function_and_package('testPackage', 'testFunction')

        ui.app.search_display.vue_update_package_object(data='testPackage')
        ui.app.search_display.vue_update_function(data='testFunction($Signal, $Signal)')

        ui.app.summary_page.selected_for_delete = 'Function: testFunction'
        ui.app.summary_page.vue_on_delete(data='')

        ui.app.search_display.vue_update_package_object(data='testPackage')

        assert 'testFunction' + '($Signal, $Signal)' not in ui.app.search_display.function_list
        assert 'testFunction' not in ui.app.search_display.function_list

    def test_archive_package(self, instantiate_ui_create_function_and_package):
        ui = instantiate_ui_create_function_and_package('testPackage', 'testFunction')

        ui.app.summary_page.selected_for_delete = 'Package: testPackage'
        ui.app.summary_page.vue_on_delete(data='')

        ui.app.search_display.vue_update_package_object(data='testPackage')

        assert 'testPackage' not in ui.app.search_display.package_list
