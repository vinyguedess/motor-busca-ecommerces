coverage run --source=app -m unittest discover -s test/* -p '*.py' -v
coverage html -d coverage
coverage xml -o coverage.xml
rm -rf .coverage