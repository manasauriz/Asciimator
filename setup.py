from setuptools import setup, find_packages

setup(
    name = 'asciimator',
    version = '1.0.0',
    packages = find_packages(),
    include_package_data=True, 
    entry_points = {
        'console_scripts': [
            'asciimator = asciimator.main:main',
        ],
    },
    install_requires = [
        "keyboard==0.13.5",
        "PyGetWindow==0.0.9",
        "pyperclip==1.9.0",
    ],
    author = "manasauriz",
    description = "A command-line tool to create and run ASCII animations!",
)