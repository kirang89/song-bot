
from setuptools import setup, find_packages
setup(
    name = "song-bot",
    version = "0.1",
    packages = find_packages(),
    scripts = ['song-bot.py',],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['requests>=1.2.3', 'BeautifulSoup>=3.2.0', 'progressbar>=2.2',],

)
