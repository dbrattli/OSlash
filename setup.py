# coding=utf-8
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools

    use_setuptools()
    from setuptools import setup

import versioneer
setup(
    name='OSlash',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="OSlash (Ø) for Python 3.8+",
    long_description=("A functional library for playing with "
                      "Functors, Applicatives, and Monads in Python."),
    author='Dag Brattli',
    author_email='dag@brattli.net',
    license='MIT License',
    url='https://github.com/dbrattli/oslash',
    download_url='https://github.com/dbrattli/oslash',
    zip_safe=True,
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['typing_extensions'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

    packages=['oslash', 'oslash.util', 'oslash.typing'],
    package_dir={'oslash': 'oslash'}
)
