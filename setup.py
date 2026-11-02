from setuptools import find_packages, setup

package_name = 'turtle_chaser'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='maulik',
    maintainer_email='maulikgpt38@gmail.com',
    description='Keyboard-controlled turtle chased by an autonomous turtle',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
           'keyboard_teleop = turtle_chaser.keyboard_teleop:main',
           'spawner = turtle_chaser.spawner:main',
           'chaser = turtle_chaser.chaser:main',
        ],
    },
)
