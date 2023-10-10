from setuptools import setup

setup(
    name="keylight-control",
    version="0.2",
    package_dir={'': 'src'},
    py_modules=["keylight_control"],
    entry_points={
        'console_scripts': [
            'keylight-control=keylight_control:main',
        ],
    },
)
