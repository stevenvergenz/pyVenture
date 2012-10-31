from setuptools import setup, find_packages

setup(
	name = 'pyVenture',
	version = '0.1',
	packages = ['pyVenture'],
	entry_points = {
		'setuptools.installation': [
			'eggsecutable = pyVenture.main:main'
		]
	}
)

setup(
	name = 'pyVentureTools',
	version = '0.1',
	packages = ['pyVentureTools'],
	entry_points = {
		'setuptools.installation': [
			'eggsecutable = pyVentureTools.main:main'
		]
	}
)
