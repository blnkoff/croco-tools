import os
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = f"{lib_folder}/requirements.txt"
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setuptools.setup(
    version='1.0.0',
    name='croco_tools',
    author='Alexey',
    author_email='abelenkov2006@gmail.com',
    description='The package containing common tools for web3-based projects.',
    keywords='croco tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/blnkoff/croco-tools',
    project_urls={
        'Documentation': 'https://github.com/blnkoff/croco-tools',
        'Bug Reports':
        'https://github.com/blnkoff/croco-tools/issues',
        'Source Code': 'https://github.com/blnkoff/croco-tools',
    },
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS'
    ],
    python_requires='>=3.11',
    install_requires=install_requires
)