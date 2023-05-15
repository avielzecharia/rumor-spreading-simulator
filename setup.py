from setuptools import find_packages, setup


setup(
    name="rumor-spreading-simulator",
    version="1.0.0",
    description='Rumor Spreading Simulator',
    author='Aviel Zecharia',
    install_requires=['matplotlib', 'easygui', 'pygame'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rumor-sim-cli = rumor_spreading_simulator.interactive.simulator_cli:main',
            'rumor-sim-stats = rumor_spreading_simulator.interactive.simulator_stats:main',
            'rumor-sim-gui = rumor_spreading_simulator.interactive.simulator_gui:main'
        ],
    }
)
