from setuptools import setup, find_packages

import attachments
version = attachments.__version__

LONG_DESCRIPTION = """
"""

setup(
    name='django-lbattachment',
    version=version,
    description="A django app to manager attachments.",
    long_description=LONG_DESCRIPTION,
    install_requires=[
        "django-helper>=0.8.1",
        "south>=0.7.2",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='attachment,django',
    author='vicalloy',
    author_email='zbirder@gmail.com',
    url='https://github.com/vicalloy/django-lbattachment/',
    license='BSD',
    packages=find_packages(),
    package_data={
        'lbattachment': [
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
