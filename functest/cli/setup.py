from setuptools import setup

setup(
    name='functest',
    version='colorado.0.1',
    py_modules=['cli_base'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        functest=cli_base:cli
    ''',
)
