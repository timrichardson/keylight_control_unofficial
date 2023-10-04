from setuptools import setup

setup(
    name="keylight-control",
    version="0.2",
    py_modules=["src"],
    entry_points={
        'console_scripts': [
            'keylight-control=keylight_control:main',
        ],
    },
)
