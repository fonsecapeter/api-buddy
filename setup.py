from distutils.core import setup
from api_buddy.constants import VERSION

setup(
    name='api-buddy',
    version=VERSION,
    author='Peter Fonseca',
    author_email='peter.nfonseca@gmail.com',
    packages=['api_buddy'],
    url='http://pypi.org/pypi/api_buddy/',
    license='MIT',
    description='',
    long_description='',
    python_requires='>3.7',
    install_requires=[
        'beautifulsoup4 == 4.7.1',
        'docopt == 0.6.2',
        'PyYAML == 4.2b1',
        'requests-oauthlib == 1.2.0',
        'schema == 0.6.8',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': [
            'api = api_buddy.cli:run',
        ],
    }
)
