"""Test the auth store."""
import json

from homeassistant.auth import auth_store, models

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

    assert len(data['refresh_tokens']) == 2
    user_token, system_token = data['refresh_tokens']

    assert user_token['token_type'] == models.TOKEN_TYPE_NORMAL
    assert user_token['last_used_at'] is None
    assert user_token['client_name'] is None
    assert user_token['client_icon'] is None
    assert user_token['last_used_ip'] is None

    assert system_token['token_type'] == models.TOKEN_TYPE_SYSTEM
    assert system_token['last_used_at'] is None
    assert system_token['client_name'] is None
    assert system_token['client_icon'] is None
    assert system_token['last_used_ip'] is None
