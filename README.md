# MkDocs Site URLs Plugin

A MkDocs plugin that adds support for site-relative `site:` URLs.

Example:

| URL | site_url | resulting URL |
| --- | -------- | ------------- |
| `site:images/foo.png` | `https://example.com/` | `/images/foo.png` |
| `site:images/foo.png` | `https://example.com/bar/` | `/bar/images/foo.png` |

**Please note**: This plugin requires MkDocs 1.5 or higher.

## Getting Started

1. Install the plugin from PyPI
   ```bash
   pip install mkdocs-site-urls
   ```
2. Add the `site-urls` plugin to your `mkdocs.yml` plugins section:
   ```yaml
   plugins:
     - site-urls
   ```
3. Start using site-relative URLs in your Markdown files by prefixing them with `site:`:
   ```markdown
   [Link to another page](site:another-page/relative/to/the/site/root)

   ![Image](site:images/foo.png)
   ```

## Configuration

By default the plugin will replace URLs in `href`, `src` and `data` attributes. You can configure the attributes to replace
by setting the `attributes` option in your `mkdocs.yml`, e.g.:

```yaml
plugins:
  - site-urls:
      attributes:
        - href
        - src
        - data
        - data-url
```

Be advised that in case of any customization on your part you need to include the default attributes as well if you want
to keep them, as the default list will not be included automatically anymore.

## How it works

The plugin hooks into the [`on_page_content` event](https://www.mkdocs.org/dev-guide/plugins/#on_page_content)
and replaces all URLs in the configured attributes (by default `href`, `src` or `data`) in the rendered HTML with the corresponding site-relative URLs.

## License

This project is licensed under the MIT license, see the [LICENSE](https://github.com/OctoPrint/mkdocs-site-urls/blob/main/LICENSE) file for details.
