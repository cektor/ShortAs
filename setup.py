from setuptools import setup

setup(
    name="ShortAs",
    version="1.0",
    packages=["shortas"],
    data_files=[("share/applications", ["shortas.desktop"])],
    entry_points={
        "console_scripts": [
            "shortas=shortas.main:main",
        ],
    },
)
