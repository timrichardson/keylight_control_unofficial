from setuptools import setup

setup(
    name="keylight_control",
    version="0.1",
    py_modules=["src"],
    entry_points={
        'console_scripts': [
            'keylight_control = keylight_control:main',
        ],
    },
)
