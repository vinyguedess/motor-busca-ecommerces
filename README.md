[![Travis](https://img.shields.io/travis/vinyguedess/motor-search-ecommerces.svg)](https://travis-ci.org/vinyguedess/motor-search-ecommerces)
[![Codecov](https://img.shields.io/codecov/c/github/vinyguedess/motor-search-ecommerces.svg)](https://codecov.io/gh/vinyguedess/motor-search-ecommerces)

# Motor de busca de ECommerces
Motor responsável por rastrear Ecommerces pela internet.

## Dependências
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Para parsear HTML
* [Flask](http://flask.pocoo.org/)
* [gunicorn](http://gunicorn.org/) - Para gerênciar a execução da aplicação
* [psycopg2](http://initd.org/psycopg/) - Para gerenciar queries executadas no Banco de Dados
* [requests](http://docs.python-requests.org/en/master/) - Para gerênciar as requests

## Instalação
Os pacotes de dependência estão todos elencados no Pipfile. Para instalar a aplicação é preciso:
```bash
    pip install pipenv
    pipenv install
```

## Executando
```bash
    gunicorn -w 4 main:app
```

## Testando
Os testes são escritos utilizando a biblioteca [unittest](https://docs.python.org/3/library/unittest.html) nativa do Python.
Também é utilizado o [coverage](https://coverage.readthedocs.io/en/coverage-4.4.1/) que coleta informações de cobertura de código.
Para que tudo rode perfeitamente, foi criado o script bash test.sh que gerência a execução dos testes.
```bash
    pip install -U coverage
    bash test.sh
```