import re

import pytest

from unittest.mock import MagicMock
from resolve_absolute_urls.plugin import ResolveAbsoluteUrlsPlugin

@pytest.fixture
def mock_plugin_config():
    return {"attributes": ["src", "href"], "prefix": "site:"}


@pytest.fixture
def create_plugin(mock_plugin_config):
    """Factory function to create the plugin with the prescribed configuration options."""

    def _plugin(config=mock_plugin_config, **kwargs):
        plugin = ResolveAbsoluteUrlsPlugin()
        plugin.load_config(config)
        for key, value in kwargs.items():
            setattr(plugin, key, value)
        return plugin

    return _plugin


@pytest.mark.parametrize(
    "attributes, prefix, string_to_match, match_group1, match_group3, should_match",
    [
        (
            ["href", "src"],
            "/docs/",
            'src = "/docs/image.png"',
            "src",
            "image.png",
            True,
        ),  # valid1
        (
            ["href", "src"],
            "/",
            "href ='/docs/image.png'",
            "href",
            "docs/image.png",
            True,
        ),  # valid2
        (
            ["data"],
            "site:",
            "data=   'site:image.png'",
            "data",
            "image.png",
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
    """Test the on_config method of the ResolveAbsoluteUrlsPlugin."""
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
    "site_url",
    [
        "https://example.com/docs/subpage/",
        "https://example.com/docs/subpage",
    ],
    ids=["trailing_slash", "no_trailing_slash"],
)
def test_on_page_content(create_plugin, site_url):
    """Test the on_page_content method of the ResolveAbsoluteUrlsPlugin."""
    plugin = create_plugin({
        "attributes": ["src", "data"],
        "prefix": "prefix",
    })
    page = MagicMock()
    config = MagicMock()
    config.__getitem__.side_effect = lambda key: site_url if key == "site_url" else None
    files = MagicMock()
    html = '''
    <img src  ="prefixexample.png" alt="Image">
    <img data =  \'prefix/image.png\'>
    <img data="site:docs/image.svg" class="example">
    <img attr  ="prefix/docs/image.png" >
    '''

    plugin.on_config(config)
    result = plugin.on_page_content(html, page, config, files)
    expected_result = '''
    <img src="/docs/subpage/example.png" alt="Image">
    <img data="/docs/subpage//image.png">
    <img data="site:docs/image.svg" class="example">
    <img attr  ="prefix/docs/image.png" >
    '''
    assert result == expected_result