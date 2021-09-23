from setuptools import setup, find_packages

setup(
    name="image-retriever",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'train=data.train:main',
        ],
    },
)
