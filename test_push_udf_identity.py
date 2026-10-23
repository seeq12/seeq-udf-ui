"""Offline unit tests for identity resolution in push_udf.

These mock the Seeq SDK Api classes and spy so they run without a live server,
and live at the repo root (not under tests/) so they are not governed by
tests/conftest.py, which requires a configured, live admin Seeq server."""
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from seeq.addons.udf_ui import backend
from seeq.addons.udf_ui.backend import _push_udfs


@pytest.fixture
def push_env(monkeypatch):
    formulas_api = MagicMock()
    formulas_api.put_package.return_value = SimpleNamespace(id='PACKAGE_ID')
    items_api = MagicMock()

    monkeypatch.setattr(_push_udfs.sdk, 'FormulasApi', lambda client: formulas_api)
    monkeypatch.setattr(_push_udfs.sdk, 'ItemsApi', lambda client: items_api)
    monkeypatch.setattr(_push_udfs.spy, 'user', SimpleNamespace(name='Tester', email='tester@example.com'))
    monkeypatch.setattr(_push_udfs.spy, 'client', MagicMock())

    return SimpleNamespace(formulas_api=formulas_api, items_api=items_api, monkeypatch=monkeypatch)


def _push(users_and_groups_list):
    return _push_udfs.push_udf(
        package_name='pkg', selected_function_name='fn', params_and_types=[],
        formula='1.toSignal()', examples_and_descriptions=[], func_description='',
        package_description='', users_and_groups_list=users_and_groups_list,
        func_id='', is_new=True)


def _acl_entries(items_api):
    return items_api.set_acl.call_args.kwargs['body']['entries']


class TestPushUdfIdentityResolution:
    def test_user_with_id_uses_it_directly(self, push_env):
        # The reported bug: editing an existing package whose ACL carries a
        # dotted/email username resolves via the id, with no username lookup.
        result = _push([{'name': 'John Doe', 'username': 'john.doe@example.com', 'type': 'User',
                         'id': 'USER_GUID', 'read': True, 'write': False, 'manage': True}])

        assert result['message_type'] == backend.MessageType.SUCCESS, result['message_content']
        assert _acl_entries(push_env.items_api) == [
            {'identityId': 'USER_GUID', 'permissions': {'read': True, 'write': False, 'manage': True}}]

    def test_group_with_id_uses_it_directly(self, push_env):
        result = _push([{'name': 'Everyone', 'username': None, 'type': 'UserGroup',
                         'id': 'EVERYONE_ID', 'read': True, 'write': False, 'manage': False}])

        assert result['message_type'] == backend.MessageType.SUCCESS, result['message_content']
        assert _acl_entries(push_env.items_api) == [
            {'identityId': 'EVERYONE_ID', 'permissions': {'read': True, 'write': False, 'manage': False}}]

    def test_entry_without_id_is_skipped_with_clear_message(self, push_env):
        result = _push([{'name': 'Everyone', 'username': None, 'type': 'UserGroup',
                         'read': True, 'write': False, 'manage': False}])

        assert result['message_type'] == backend.MessageType.ERROR
        assert "Could not set permissions for 'Everyone' because it has no identity id" in result['message_content']
        assert 'Traceback' not in result['message_content']
        assert _acl_entries(push_env.items_api) == []
