import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="khlbot-bcc",
    version="1.0.2",
    author="purofle",
    author_email="3272912942@qq.com",
    description="开黑啦 Bot websocket API 的 Python 实现.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/purofle/khlbot",
    project_urls={
        "Bug Tracker": "https://github.com/purofle/khlbot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=["graia-broadcast"],
)
