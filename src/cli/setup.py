#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# setuptools v42.0.0+
# wheel v0.37.0+
import os
import re
from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'A production-ready command-line to-do list application for efficient task management'
AUTHOR = 'Project Author'
AUTHOR_EMAIL = 'author@example.com'

def read_requirements():
    """
    Securely reads and validates package requirements from requirements.txt
    Returns a sanitized list of package requirements
    """
    requirements = []
    try:
        req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
        with open(req_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    # Validate requirement format
                    if re.match(r'^[A-Za-z0-9][A-Za-z0-9._-]*[A-Za-z0-9]([><=!~]=?[0-9.*]+)?$', line):
                        requirements.append(line)
                    else:
                        raise ValueError(f'Invalid requirement format: {line}')
    except FileNotFoundError:
        print('Warning: requirements.txt not found. Using default requirements.')
        requirements = ['setuptools>=42.0.0', 'wheel>=0.37.0']
    except Exception as e:
        print(f'Error reading requirements: {str(e)}')
        raise
    return requirements

def read_readme():
    """
    Reads and validates the long description from README.md
    Returns the validated content of README.md
    """
    try:
        readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Basic markdown validation
            if not content or len(content.strip()) < 10:
                raise ValueError('README.md appears to be empty or too short')
            return content
    except FileNotFoundError:
        print('Warning: README.md not found. Using default description.')
        return DESCRIPTION
    except Exception as e:
        print(f'Error reading README: {str(e)}')
        raise

def read_license():
    """
    Reads and validates the license file content
    Returns the content of LICENSE file
    """
    try:
        license_path = os.path.join(os.path.dirname(__file__), 'LICENSE')
        with open(license_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Basic license validation
            if not content or 'MIT License' not in content:
                raise ValueError('LICENSE file appears invalid or not MIT')
            return content
    except FileNotFoundError:
        print('Warning: LICENSE file not found.')
        return None
    except Exception as e:
        print(f'Error reading license: {str(e)}')
        raise

setup(
    name='simple-todo-cli',
    version=VERSION,
    description=DESCRIPTION,
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license='MIT',
    python_requires='>=3.6',
    packages=find_packages(exclude=['tests*', 'docs*']),
    install_requires=read_requirements(),
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'todo=cli.main:main',
        ],
    },
    package_data={
        'cli': ['LICENSE', 'README.md', 'requirements.txt'],
    },
    project_urls={
        'Source': 'https://github.com/username/simple-todo-cli',
        'Bug Reports': 'https://github.com/username/simple-todo-cli/issues',
        'Documentation': 'https://github.com/username/simple-todo-cli/wiki',
    },
    keywords=[
        'todo',
        'cli',
        'task-management',
        'productivity',
        'command-line',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Office/Business :: Scheduling',
        'Topic :: Utilities',
        'Natural Language :: English',
        'Typing :: Typed',
    ],
)