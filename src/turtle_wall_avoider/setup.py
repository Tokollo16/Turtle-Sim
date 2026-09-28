from setuptools import find_packages, setup

package_name = 'turtle_wall_avoider'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ROS 2 User',
    maintainer_email='user@example.com',
    description='Moves a turtlesim turtle around an inset route without hitting the walls.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'wall_avoider = turtle_wall_avoider.wall_avoider:main',
        ],
    },
)
