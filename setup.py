from setuptools import setup, find_packages

_version = {}
with open('pywig/_version.py') as fp:
    exec(fp.read(), _version)

tests_require = []

name = 'pywig'
setup(name=name,
      version=_version['__version__'],
      author='VITO',
      description='Python Client API for WatchItGrow',
      url="https://watchitgrow.be",
      python_requires=">=3.6",
      packages=find_packages(),
      tests_require=tests_require,
      test_suite='tests',
      install_requires=[
          'requests',
          'oauthlib',
          'requests_oauthlib',
          'shapely'
      ],
      include_package_data=True,
      package_data={
          "": ["**/*.conf"],
      },
      extras_require={
          "dev": tests_require + []
      },
      )
