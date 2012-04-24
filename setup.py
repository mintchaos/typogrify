from setuptools import setup, find_packages


setup(
    name='typogrify',
    version='1.0.1a',
    packages=find_packages(),
    author='Christian Metts',
    author_email='xian@mintchaos.com',
    license='BSD',
    description='Typography related template filters for Django & Jinja2 applications',
    url='https://github.com/mintchaos/typogrify',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Utilities'
    ],

    install_requires=['smartypants>=1.6']
)