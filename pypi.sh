pip install wheel
pip install twine
rm -rf build
rm -rf dist
rm -rf afpy.egg.info
python setup.py sdist bdist_wheel
python -m twine upload dist/*