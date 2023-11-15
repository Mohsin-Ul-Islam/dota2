"""Test suite for dota2 config/metadata."""

from expects import equal, expect

from dota2 import __version__


def test_version():
    """Assert that the package version is correct."""

    expect(__version__).to(equal("0.1.0"))
