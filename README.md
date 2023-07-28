# MkDocs Site URLs

A MkDocs plugin that adds support for site-relative `site:` URLs.

Example:

| URL | site_url | resulting URL |
| --- | -------- | ------------- |
| `site:images/foo.png` | `https://example.com/` | `/images/foo.png` |
| `site:images/foo.png` | `https://example.com/bar/` | `/bar/images/foo.png` |

## Usage

1. Install the plugin from PyPI
   ```bash
   pip install mkdocs-site-urls
   ```
2. Add the `site-urls` plugin to your `mkdocs.yml` plugins section:
   ```yaml
   plugins:
     - site-urls
   ```
   There are no configuration options.
3. Start using site-relative URLs in your Markdown files by prefixing them with `site:`:
   ```markdown
   [Link to another page](site:another-page/relative/to/the/site/root)

   ![Image](site:images/foo.png)
   ```

## How it works

The plugin hooks into the [`on_page_content` event](https://www.mkdocs.org/dev-guide/plugins/#on_page_content)
and replaces all URLs in `href` or `src` attributes in the rendered HTML with the corresponding site-relative URLs.

## License

This project is licensed under the MIT license, see the [LICENSE](https://github.com/OctoPrint/mkdocs-site-urls/blob/main/LICENSE) file for details.
