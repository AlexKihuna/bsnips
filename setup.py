from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='bsnips',
      version='0.0.1',
      description='A collection of random but useful util code.',
      long_description=readme(),
      classifiers=[
          'Development Status :: 1 - Planning',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities',
      ],
      keywords='utilities',
      test_suite='nose.collector',
      tests_require=['nose'],
      url='http://github.com/alexkihuna/bsnips',
      author='Alex Kihuna',
      entry_points={
          'console_scripts': ['file_dupe=bsnips.file_dupe:main'],
      },
      license='MIT',
      packages=['bsnips'],
      install_requires=[
          'requests', 'peewee'
      ],
      zip_safe=False)
