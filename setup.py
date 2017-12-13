from setuptools import setup

setup(
    name='moody',
    packages=['moody'],
    include_package_data=True,
    install_requires=[
        'arrow',
        'bcrypt',
        'Flask',
        'Flask-Cors',
        'marshmallow',
        'PyJWT',
        'requests',
        'SQLAlchemy',
    ],
)
