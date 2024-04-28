from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='pymesomb',
    version='1.0.4',
    description='Python client for MeSomb services.',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Hachther LLC',
    author_email='contact@hachther.com',
    keywords=['MeSomb', 'MobileMoney', 'OrangeMoney'],
    url='https://github.com/hachther/mesomb-python-client.git',
    download_url='https://pypi.org/project/pymesomb/'
)

install_requires = [
    'requests',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
