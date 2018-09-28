"""Test the auth store."""
import json

from homeassistant.auth import auth_store

from tests.common import load_fixture


async def test_migration_v1_v2(hass, hass_storage):
    """Test migrating auth store to add groups."""
    hass_storage[auth_store.STORAGE_KEY] = json.loads(
        load_fixture('auth_v1.json'))
    store = auth_store.DataStore(hass)
    data = await store.async_load()

    assert len(data['groups']) == 2
    system_group, family_group = data['groups']

    assert system_group['system_generated'] is True
    assert system_group['name'] == 'System'

    assert family_group['system_generated'] is False
    assert family_group['name'] == 'Family'

    assert len(data['users']) == 2
    owner, hassio = data['users']

    assert owner['is_owner'] is True
    assert owner['group_id'] == family_group['id']

    assert hassio['is_owner'] is False
    assert hassio['group_id'] == system_group['id']
