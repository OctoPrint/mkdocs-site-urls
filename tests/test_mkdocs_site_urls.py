import re
from unittest.mock import MagicMock

import pytest

from mkdocs_site_urls import SiteUrlsPlugin


@pytest.fixture
def mock_plugin_config():
    return {"attributes": ["src", "href"], "prefix": "site:"}


@pytest.fixture
def create_plugin(mock_plugin_config):
    """Factory function to create the plugin with the prescribed configuration options."""

    def _plugin(config=mock_plugin_config, **kwargs):
        plugin = SiteUrlsPlugin()
        plugin.load_config(config)
        for key, value in kwargs.items():
            setattr(plugin, key, value)
        return plugin

    return _plugin


@pytest.mark.parametrize(
    "attributes, prefix, string_to_match, match_group1, match_group3, should_match",
    [
        (
            ["data"],
            "site:",
            "data=   'site:image.png'",
            "data",
            "image.png",
            True,
        ),  # valid1
        (
            ["href", "src"],
            "/docs/",
            'src = "/docs/image.png"',
            "src",
            "image.png",
            True,
        ),  # valid2
        (
            ["href", "src"],
            "/",
            "href ='/docs/image.png'",
            "href",
            "docs/image.png",
            True,
        ),  # valid3
        (
            ["href", "src"],
            "/docs/",
            'src = "/image.png"',
            None,
            None,
            False,
        ),  # invalid_different_prefix
        (
            ["href", "src"],
            "/",
            "href ='site:docs/image.png'",
            None,
            None,
            False,
        ),  # invalid_different_prefix2
        (
            ["data"],
            "/",
            "href='/image.png'",
            None,
            None,
            False,
        ),  # invalid_different_attribute
    ],
    ids=[
        "valid1",
        "valid2",
        "valid3",
        "invalid_different_prefix",
        "invalid_different_prefix2",
        "invalid_different_attribute",
    ],
)
def test_on_config_sets_regex(
    create_plugin,
    attributes,
    prefix,
    string_to_match,
    match_group1,
    match_group3,
    should_match,
):
    """Test the on_config method of the SiteUrlsPlugin."""
    plugin_config = {
        "attributes": attributes,
        "prefix": prefix,
    }
    plugin = create_plugin(plugin_config)
    plugin.on_config(MagicMock())

    # Check that the regex is compiled
    assert isinstance(plugin._regex, re.Pattern)
    match = plugin._regex.search(string_to_match)

    # Check regex is correct
    if should_match:
        assert match is not None
        assert match.group(1) == match_group1
        assert match.group(3) == match_group3
    else:
        assert match is None


@pytest.mark.parametrize(
    "prefix, site_url, expected_path",
    [
        ("site:", "https://example.com", "/"),
        ("site:", "https://example.com/docs/subpage/", "/docs/subpage/"),
        ("site:", "https://example.com/docs/subpage", "/docs/subpage/"),
        ("site:", None, "/"),
        ("site:", "", "/"),
        ("prefix", None, "/"),
        ("/", "https://example.com/docs/subpage/", "/docs/subpage/"),
    ],
    ids=[
        "basic",
        "path_trailing_slash",
        "path_no_trailing_slash",
        "none_siteurl",
        "empty_siteurl",
        "custom_prefix",
        "slash_as_prefix",
    ],
)
def test_on_page_content(create_plugin, prefix, site_url, expected_path):
    """Test the on_page_content method of the SiteUrlsPlugin."""
    plugin = create_plugin(
        {
            "attributes": ["src", "data", "href"],
            "prefix": prefix,
        }
    )
    page = MagicMock()
    config = MagicMock()
    config.get.side_effect = (
        lambda key, default=None: site_url
        if key == "site_url" and site_url is not None
        else default
    )
    files = MagicMock()

    html = f"""
    <img src  ="{prefix}example.png" alt="Image">
    <img data =  \'{prefix}/image.png\'>
    <img data="{prefix}docs/image.svg" class="example">
    <img attr  ="{prefix}/docs/image.png" title="this won't get touched, wrong attribute" >
    <img href = "NOT_A_PREFIX/foo/image.png" title="neither will this, wrong prefix">
    """

    plugin.on_config(config)
    result = plugin.on_page_content(html, page, config, files)
    expected_result = f"""
    <img src="{expected_path}example.png" alt="Image">
    <img data="{expected_path}/image.png">
    <img data="{expected_path}docs/image.svg" class="example">
    <img attr  ="{prefix}/docs/image.png" title="this won't get touched, wrong attribute" >
    <img href = "NOT_A_PREFIX/foo/image.png" title="neither will this, wrong prefix">
    """
    assert result == expected_result
