from setuptools import find_packages, setup

setup(
    name="simple_crawler",
    version="0.0.1",
    url="https://github.com/raj457036/Simple-Web-Crawler",
    project_urls={
        "Source": "https://github.com/raj457036/Simple-Web-Crawler",
        "Tracker": "https://github.com/raj457036/Simple-Web-Crawler/issues",
    },
    description="A simple web crawler with async and sync support.",
    author="Raj Singh",
    author_email="rs457036@gmail.com",
    maintainer="Raj Singh",
    maintainer_email="rs457036@gmail.com",
    license="MIT",
    packages=find_packages(
        where="./webcrawler",
        exclude=("tests", "tests.*"),
    ),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[
        "beautifulsoup4>=4.12.2",
        "httpx>=0.25.0",
        "markdownify>=0.11.6",
        "pydantic>=2.3.0",
        "urllib3>=2.0.4",
        "coloredlogs>=15.0.1",
        "aiofiles>=23.2.1",
    ],
)
