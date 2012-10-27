from setuptools import setup, find_packages

setup(
	name = 'pyVenture',
	version = '0.1',
	packages = find_packages(),
	entry_points = {
		'setuptools.installation': [
			'eggsecutable = pyVenture.main:main'
		]
	}
)


