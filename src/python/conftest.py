# -*- coding: utf-8 -*-
"""
Setup localstack AWS environment variables for pytest
"""
import pytest


@pytest.fixture
def set_localstack_env_vars(monkeypatch):
    """
    mocks localstack AWS environment variables for pytest
    @param monkeypatch: pytest monkeypatch
    @return:
    """
    env = {
        "AWS_USE_SSL": "False",
        "AWS_VERIFY": "False",
        "AWS_ENDPOINT_URL": "http://127.0.0.1:4566",
        "AWS_ACCESS_KEY_ID": "dummy-access-key-id",
        "AWS_ACCESS_KEY": "dummy-access-key",
        "AWS_SECRET_ACCESS_KEY": "dummy-test-secret-key",
        "AWS_SECRET_KEY": "dummy-test-secret-key",
        "AWS_DEFAULT-REGION": "us-east-1"
    }
    # add localstack environment variables to monkeypatch
    # to use in pytest
    for key, value in env.items():
        monkeypatch.setenv(key, value)
