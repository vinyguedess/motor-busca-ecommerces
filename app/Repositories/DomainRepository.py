from json import dumps
from app.Entities.Domain import Domain
from app.Core import ErrorsManager


class DomainRepository(ErrorsManager):

    _conn = None

    def __init__(self, conn):
        self._conn = conn

    def insert(self, domain):
        try:
            query = "INSERT INTO domains (domain, hubspot_id, metadata) VALUES (%s, %s, %s) RETURNING id;"

            cursor = self._conn.getConn()
            cursor.execute(query, [ domain.domain, domain.hubspot_id, dumps(domain.metadata) ])
            self._conn.commit()

            domain.id = cursor.fetchone()[0]

            return True
        except Exception as ex:
            self._conn.rollback()
            self.addError(ex.args)
            return False

    def update(self, domain):
        try:
            if not domain.id:
                raise Exception("ID required before updating Entity")

            query = "UPDATE domains SET hubspot_id = %s, metadata = %s WHERE id = %s;"

            cursor = self._conn.getConn()
            cursor.execute(query, [ domain.hubspot_id, dumps(domain.metadata), domain.id ])
            self._conn.commit()

            return True
        except Exception as ex:
            self._conn.rollback()
            self.addError(ex.args)
            return False

    def find_by_id(self, id):
        query = "SELECT * FROM domains WHERE id = %s;"

        cursor = self._conn.getConn()
        cursor.execute(query, [ id ])
        
        result = cursor.fetchone()
        if not result:
            return None
        
        return self.map_domain_to_object(result)

    def map_domain_to_object(self, result):
        domain = Domain()
        domain.id = result[0]
        domain.hubspot_id = result[3]
        domain.domain = result[1]
        domain.metadata = result[2]

        return domain

    def check_if_domain_exists(self, domain):
        query = "SELECT COUNT(*) AS total FROM domains WHERE domain = '%s';"

        cursor = self._conn.getConn()
        cursor.execute(query % domain)
        result = cursor.fetchone()

        return result[0] > 0