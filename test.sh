coverage run -m unittest discover -s test/* -p '*.py' -v
coverage html -d coverage
rm -rf .coverage