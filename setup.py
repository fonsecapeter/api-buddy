from distutils.core import setup

setup(
    name='ttam-buddy',
    version='0.1.0',
    author='Peter Fonseca',
    author_email='peter.nfonseca@gmail.com',
    packages=['ttam_buddy'],
    url='http://pypi.org/pypi/ttam_buddy/',
    license='MIT',
    description='',
    long_description='',
    install_requires=[
        'click == 7.0',
        'PyYAML == 3.13',
        'requests-oauthlib == 1.2.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'ttam-buddy = ttam_buddy.cli:run',
        ],
    }
)
