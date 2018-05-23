from setuptools import setup

# Extract version
def get_version():
    with open('plotmenow/plotmenow.py') as f:
        for line in f.readlines():
            if "__version__" in line:
                return line.split('"')[1]

def setup_package():

    metadata = dict(
        name='plotmenow',
        version=get_version(),
        description='Python decorator to handle matplotlib options',
        long_description="See: `github.com/dgerosa/plotmenow <https://github.com/dgerosa/plotmenow>`_." ,
        url='https://github.com/dgerosa/plotmenow',
        author='Davide Gerosa',
        author_email='dgerosa@caltech.edu',
        license='MIT',
        packages=['plotme'],
        install_requires=['matplotlib'],
        include_package_data=True,
        zip_safe=False,
    )

    setup(**metadata)


if __name__ == '__main__':

    setup_package()
