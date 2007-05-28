from distutils.core import setup

setup(name='typogrify',
      version='0.1',
      description='Typography related template filters for Django applications',
      author='Christian Metts',
      author_email='xian@mintchaos.com',
      url='http://code.google.com/p/typogrify/',
      packages=['typogrify', 'typogrify.templatetags'],
      classifiers=['Development Status :: 1 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers :: Designers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      )
