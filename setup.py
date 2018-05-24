#python setup.py sdist upload -r test
#python setup.py sdist upload

from setuptools import setup

# Extract version
def get_version():
    with open('skywalker/skywalker.py') as f:
        for line in f.readlines():
            if "__version__" in line:
                return line.split('"')[1]

def setup_package():

    metadata = dict(
        name='skywalker',
        version=get_version(),
        description='Things I like in python',
        long_description="`https://github.com/dgerosa/skywalker <https://github.com/dgerosa/skywalker>`_" ,
        url='https://github.com/dgerosa/skywalker',
        author='Davide Gerosa',
        author_email='dgerosa@caltech.edu',
        license='MIT',
        packages=['skywalker'],
        install_requires=['matplotlib','tqdm'],
        include_package_data=True,
        zip_safe=False,
    )

    setup(**metadata)


if __name__ == '__main__':

    setup_package()
