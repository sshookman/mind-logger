from setuptools import setup, find_packages

setup(
    name='mindlogger',
    version='0.4.0',
    description='A Logging Framework For Your Mind',
    author='Sean Shookman',
    author_email='sms112788@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'mindlogger = mindlogger:main',
        ],
    }
)
