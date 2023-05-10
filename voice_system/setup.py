from setuptools import setup

package_name = 'voice_system'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ri-one',
    maintainer_email='rione.homeleague@gmail.com',
    description='Ri-one voice system',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'text_to_speech = voice_system.tts_server:main',
            'speech_to_text = voice_system.stt_server:main',
        ],
    },
)
