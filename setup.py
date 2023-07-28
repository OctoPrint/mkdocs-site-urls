from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mkdocs-site-urls",
    version="0.1.0",
    author="Gina Häußge",
    author_email="gina@octoprint.org",
    url="https://github.com/OctoPrint/mkdocs-site-urls",
    project_urls={"Source": "https://github.com/OctoPrint/mkdocs-site-urls"},
    keywords=["mkdocs", "plugin"],
    packages=find_packages(),
    license="MIT",
    description="A MkDocs plugin that adds support for site-relative URLs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.7",
    entry_points={"mkdocs.plugins": ["site-urls = mkdocs_site_urls:SiteUrlsPlugin"]},
)
