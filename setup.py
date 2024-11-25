from pathlib import Path
from pkg_resources import parse_requirements
from setuptools import find_packages, setup

setup(
    name="send_linkedin_msg_pkg",
    author="Quyen Do",
    author_email="quyen.do@orientsoftware.com",
    packages=find_packages()
)