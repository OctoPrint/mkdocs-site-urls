import re
import urllib.parse

import mkdocs.plugins
from mkdocs.config import config_options as c
from mkdocs.config.defaults import MkDocsConfig

logger = mkdocs.plugins.get_plugin_logger(__name__)


class SiteUrlsConfig(mkdocs.config.base.Config):
    attributes = c.Type(list, default=["href", "src", "data"])


class SiteUrlsPlugin(mkdocs.plugins.BasePlugin[SiteUrlsConfig]):
    def on_pre_build(self, *, config: MkDocsConfig) -> None:
        self._regex = re.compile(
            r"(" + "|".join(self.config["attributes"]) + r')="site:([^"]+)"',
            re.IGNORECASE,
        )

    @mkdocs.plugins.event_priority(50)
    def on_page_content(self, html, page, config, files):
        site_url = config["site_url"]
        path = urllib.parse.urlparse(site_url).path

        if not path:
            path = "/"
        if not path.endswith("/"):
            path += "/"

        def _replace(match):
            param = match.group(1)
            url = match.group(2)
            if url.startswith("/"):
                url = url[1:]

            logger.info(f"Replacing site:{match.group(2)} with {path}{url}")
            return f'{param}="{path}{url}"'

        return self._regex.sub(_replace, html)
