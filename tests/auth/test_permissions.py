"""Tests for the auth permission system."""
import pytest

from homeassistant.core import State
from homeassistant.auth import permissions


@pytest.fixture
def perm():
    """Fixture permission object."""
    perm = permissions.Permissions()
    perm.mock_policy = permissions.DEFAULT_POLICY
    perm._resolve_policy = lambda user_id: perm.mock_policy
    return perm


def test_entities_none():
    """Test entity ID policy."""
    policy = None
    compiled = permissions._compile_entities(policy)
    assert not compiled('light.kitchen', [])


def test_entities_empty():
    """Test entity ID policy."""
    policy = {}
    permissions.ENTITY_POLICY_SCHEMA(policy)
    compiled = permissions._compile_entities(policy)
    assert not compiled('light.kitchen', [])


def test_entities_false():
    """Test entity ID policy."""
    policy = False
    permissions.ENTITY_POLICY_SCHEMA(policy)
    compiled = permissions._compile_entities(policy)
    assert not compiled('light.kitchen', [])


def test_entities_true():
    """Test entity ID policy."""
    policy = True
    permissions.ENTITY_POLICY_SCHEMA(policy)
    compiled = permissions._compile_entities(policy)
    assert compiled('light.kitchen', [])


def test_entities_domains_true():
    """Test entity ID policy."""
    policy = {
        'domains': True
    }
    permissions.ENTITY_POLICY_SCHEMA(policy)
    compiled = permissions._compile_entities(policy)
    assert compiled('light.kitchen', [])


def test_entities_domains_false():
    """Test entity ID policy."""
    policy = {
        'domains': False
    }
    permissions.ENTITY_POLICY_SCHEMA(policy)
    compiled = permissions._compile_entities(policy)
    assert not compiled('light.kitchen', [])


def test_entities_domains_domain_true():
    """Test entity ID policy."""
    policy = {
        'domains': {
            'light': True
        }
    }
    permissions.ENTITY_POLICY_SCHEMA(policy)
    compiled = permissions._compile_entities(policy)
    assert compiled('light.kitchen', [])
    assert not compiled('switch.kitchen', [])


def test_entities_domains_domain_false():
    """Test entity ID policy."""
    policy = {
        'domains': {
            'light': False
        }
    }
    permissions.ENTITY_POLICY_SCHEMA(policy)
    compiled = permissions._compile_entities(policy)
    assert not compiled('light.kitchen', [])
    assert not compiled('switch.kitchen', [])


def test_entities_entity_ids_true():
    """Test entity ID policy."""
    policy = {
        'entity_ids': True
    }
    permissions.ENTITY_POLICY_SCHEMA(policy)
    compiled = permissions._compile_entities(policy)
    assert compiled('light.kitchen', [])


def test_entities_entity_ids_false():
    """Test entity ID policy."""
    policy = {
        'entity_ids': False
    }
    permissions.ENTITY_POLICY_SCHEMA(policy)
    compiled = permissions._compile_entities(policy)
    assert not compiled('light.kitchen', [])


def test_entities_entity_ids_entity_id_true():
    """Test entity ID policy."""
    policy = {
        'entity_ids': {
            'light.kitchen': True
        }
    }
    permissions.ENTITY_POLICY_SCHEMA(policy)
    compiled = permissions._compile_entities(policy)
    assert compiled('light.kitchen', [])
    assert not compiled('switch.kitchen', [])


def test_entities_entity_ids_entity_id_false():
    """Test entity ID policy."""
    policy = {
        'entity_ids': {
            'light.kitchen': False
        }
    }
    permissions.ENTITY_POLICY_SCHEMA(policy)
    compiled = permissions._compile_entities(policy)
    assert not compiled('light.kitchen', [])
    assert not compiled('switch.kitchen', [])


def test_filter_entities(perm):
    """Test filtering entitites."""
    states = [
        State('light.kitchen', 'on'),
        State('light.living_room', 'off'),
        State('light.balcony', 'on'),
    ]
    perm.mock_policy = {
        'entities': {
            'entity_ids': {
                'light.kitchen': True,
                'light.balcony': True,
            }
        }
    }
    filtered = perm.filter_entities('mock-user-id', states)
    assert len(filtered) == 2
    assert filtered == [states[0], states[2]]
