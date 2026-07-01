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
    def test_uses_id_directly_without_searching(self, push_env):
        # The reported bug: editing an existing package whose ACL carries a
        # dotted/email username must resolve via the id and never search.
        push_env.monkeypatch.setattr(_push_udfs, '_get_user',
                                     MagicMock(side_effect=AssertionError('must not search when id is present')))
        push_env.monkeypatch.setattr(_push_udfs, '_get_user_group',
                                     MagicMock(side_effect=AssertionError('must not search when id is present')))

        result = _push([{'name': 'John Doe', 'username': 'john.doe@example.com', 'type': 'User',
                         'id': 'USER_GUID', 'read': True, 'write': False, 'manage': True}])

        assert result['message_type'] == backend.MessageType.SUCCESS, result['message_content']
        assert _acl_entries(push_env.items_api) == [
            {'identityId': 'USER_GUID', 'permissions': {'read': True, 'write': False, 'manage': True}}]

    def test_fallback_searches_raw_username_and_matches_exactly(self, push_env):
        found = SimpleNamespace(users=[SimpleNamespace(username='john.doe', id='DECOY'),
                                       SimpleNamespace(username='john.doe@example.com', id='FOUND_ID')])
        get_user = MagicMock(return_value=found)
        push_env.monkeypatch.setattr(_push_udfs, '_get_user', get_user)

        result = _push([{'name': 'John Doe', 'username': 'john.doe@example.com', 'type': 'User',
                         'read': True, 'write': True, 'manage': False}])

        assert result['message_type'] == backend.MessageType.SUCCESS, result['message_content']
        get_user.assert_called_once_with('john.doe@example.com')  # raw username, not re.escape-d
        assert _acl_entries(push_env.items_api)[0]['identityId'] == 'FOUND_ID'

    def test_missing_user_reports_clean_message_without_traceback(self, push_env):
        push_env.monkeypatch.setattr(_push_udfs, '_get_user',
                                     MagicMock(return_value=SimpleNamespace(users=[])))

        result = _push([{'name': 'Ghost User', 'username': 'ghost.user@example.com', 'type': 'User',
                         'read': True, 'write': False, 'manage': False}])

        assert result['message_type'] == backend.MessageType.ERROR
        assert "Could not find the user 'Ghost User'" in result['message_content']
        assert 'Traceback' not in result['message_content']
        assert _acl_entries(push_env.items_api) == []

    def test_group_fallback_matches_by_exact_name(self, push_env):
        groups = SimpleNamespace(items=[SimpleNamespace(name='EveryoneElse', id='WRONG'),
                                        SimpleNamespace(name='Everyone', id='EVERYONE_ID')])
        push_env.monkeypatch.setattr(_push_udfs, '_get_user_group', MagicMock(return_value=groups))

        result = _push([{'name': 'Everyone', 'username': None, 'type': 'UserGroup',
                         'read': True, 'write': False, 'manage': False}])

        assert result['message_type'] == backend.MessageType.SUCCESS, result['message_content']
        assert _acl_entries(push_env.items_api)[0]['identityId'] == 'EVERYONE_ID'
