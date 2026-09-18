from __future__ import annotations

import pytest

from app import create_app

from .kit import build_repo


@pytest.fixture
def repo(tmp_path):
    return build_repo(tmp_path)


@pytest.fixture
def vault_root(repo):
    return repo / "docs-arc42-brain"


@pytest.fixture
def client(repo):
    return create_app(repo).test_client()
