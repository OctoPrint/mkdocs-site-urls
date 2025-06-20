import re
import urllib.parse

import mkdocs.plugins
from mkdocs.config import config_options as c
from mkdocs.config.defaults import MkDocsConfig

logger = mkdocs.plugins.get_plugin_logger(__name__)


class Config(mkdocs.config.base.Config):
    attributes = c.Type(list, default=["href", "src", "data"])
    prefix = c.Type(str, default="site:")


class SiteUrlsPlugin(mkdocs.plugins.BasePlugin[Config]):
    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        attributes = (re.escape(attr) for attr in self.config["attributes"])
        self.prefix = re.escape(self.config["prefix"])
        regex_parts = [
            r"(",  # capturing group 1
            "|".join(attributes),  # attributes
            r")",  # end of capturing group 1
            r"\s*=\s*",  # equals sign with optional whitespace
            r"([\"'])",  # quote with capturing group 2
            self.prefix,  # url prefix
            r"([^\"']*)",  # remainder of the url with capturing group 3
            r"\2",  # matching quote
        ]
        regex = "".join(regex_parts)
        self._regex = re.compile(regex, re.IGNORECASE)
        return config

    @mkdocs.plugins.event_priority(50)
    def on_page_content(self, html, page, config, files):
        site_url = config["site_url"]
        if not site_url.endswith("/"):
            site_url += "/"
        path = urllib.parse.urlparse(site_url).path

        def _replace(match):
            attribute = match.group(1)
            url = match.group(3)

            logger.info(f"Replacing absolute url '{self.prefix}{url}' with '{path}{url}'")
            return f'{attribute}="{path}{url}"'

        return self._regex.sub(_replace, html)
