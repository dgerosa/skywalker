#python setup.py sdist upload -r test
#python setup.py sdist upload

from setuptools import setup

def get_meta(metaname):
    with open('skywalker/skywalker.py') as f:
        for line in f.readlines():
            if "__"+metaname+"__" in line and "__main__" not in line:
                return line.split('"')[1]

setup(
    name=get_meta('name'),
    version=get_meta('version'),
    description=get_meta('description'),
    license=get_meta('license'),
    author=get_meta('author'),
    author_email=get_meta('author_email'),
    url=get_meta('url'),
    long_description="See: `"+get_meta('url')+" <"+get_meta('url')+">`_." ,
    packages=[get_meta('name')],
    install_requires=['matplotlib','tqdm','ediblepickle','deepdish','contexttimer','singleton_decorator'],
    include_package_data=True,
    zip_safe=False,
)
