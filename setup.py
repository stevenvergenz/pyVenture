from setuptools import setup, find_packages

setup(
	name = 'pySOG',
	version = '0.1',
	packages = find_packages(),
	entry_points = {
		'setuptools.installation': [
			'eggsecutable = pysog.main:main'
		]
	}
)


