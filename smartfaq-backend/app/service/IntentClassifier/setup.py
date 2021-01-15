from distutils.core import setup
setup(
  name = 'IntentClassifier',
  packages = ['IntentClassifier'],
  version = '0.1',
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A package for intent classifier',
  author = 'Toriq Ahmad Salam',
  author_email = 'toriqahmads@gmail.com',
  url = 'https://github.com/toriqahmads/inten-classifier-lstm',
  download_url = 'https://github.com/toriqahmads/inten-classifier-lstm/archive/v_01.tar.gz',
  keywords = ['nlp', 'intent classifier', 'lstm', 'rnn', 'deep learning'],
  install_requires=[
    'tensorflow>=2.2.0',
    'sklearn',
    'keras>=2.4.2',
    'pickle',
    'Sastrawi>=1.0.1',
    'pandas>=1.0.5',
    'numpy>=1.19.0',
    'tensorboard>=2.2.2',
    'grpcio>=1.30.0'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)