from json import dumps


class DomainService():

    _conn = None

    def __init__(self, conn):
        self._conn = conn

    def insert_domain(self, domain):
        try:
            query = "INSERT INTO domains (domain, hubspot_id, metadata) VALUES (%s, %s, %s) RETURNING id;"

            cursor = self._conn.getConn()
            cursor.execute(query, [ domain.domain, domain.hubspot_id, dumps(domain.metadata) ])
            self._conn.commit()

            domain.id = cursor.fetchone()[0]

            return True
        except Exception as ex:
            self._conn.rollback()
            return False

    def update_domain(self, domain):
        try:
            query = "UPDATE domains SET hubspot_id = %s, metadata = %s WHERE id = %s;"

            cursor = self._conn.getConn()
            cursor.execute(query, [ domain.hubspot_id, dumps(domain.metadata), domain.id ])
            self._conn.commit()

            return True
        except Exception as ex:
            print(ex)
            self._conn.rollback()
            return False

    def check_if_domain_exists(self, domain):
        query = "SELECT COUNT(*) AS total FROM domains WHERE domain = '%s';"

        cursor = self._conn.getConn()
        cursor.execute(query % domain)
        result = cursor.fetchone()

        return result[0] > 0