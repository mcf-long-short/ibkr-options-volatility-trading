from setuptools import setup, find_packages

from market_watcher.version import VERSION


setup(
    name="market_watcher",
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "market_watcher_cli = market_watcher.market_watcher_cli:cli",
        ],
    },
)
