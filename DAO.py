# Data Access Objects:
# All of these are meant to be singletons
import DTO
import sqlite3
class _Vaccines:
    def __init__(self, conn):
        self._conn = conn
    
    def insert(self, vaccine):
        self._conn.execute("""
                INSERT INTO vaccines (date, supplier, quantity) VALUES (?, ?, ?)
            """, [vaccine.date, vaccine.supplier, vaccine.quantity])
    
    def find(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM vaccines WHERE id = ?
        """, [vaccine_id])
    
        return Vaccine(*c.fetchone())
    
    
class _Suppliers:
    def __init__(self, conn):
        self._conn = conn
    
    def insert(self, supplier):
        self._conn.execute("""
                INSERT INTO suppliers (id, name, logistic) VALUES (?, ?, ?)
        """, [supplier.id, supplier.name, supplier.logistic])
    
    def findByID(self, supplier_id):
        c = self._conn.cursor()
        c.execute("""
                SELECT * FROM suppliers WHERE id = ?
            """, [supplier_id])

    def findByName(self, sup_name):
        c = self._conn.cursor()
        c.execute("""
                SELECT id FROM suppliers WHERE name = ?
            """, [sup_name])    
        return c.fetchone()
    
    
class _Clinics:
    def __init__(self, conn):
        self._conn = conn
    
    def insert(self, clinic):
        self._conn.execute("""
            INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
        """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT * FROM clinics
        """).fetchall()
    
        return [Clinic(*row) for row in all]

      
      
class _Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""
            INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
        """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT * FROM logistics
        """).fetchall()

        return [Logistic(*row) for row in all]