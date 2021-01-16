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

    def getVaccineToSend(self):
        c = self._conn.cursor()
        c.execute("""
                SELECT * FROM vaccines ORDER BY(date) ASC 
        """)
        return Vaccine(*c.fetchone())

    def deleteVacc(self, vacc_id):    
        self._conn.execute("""
                DELETE FROM vaccines WHERE id = ? 
        """, [vacc_id])

    def updateQuantity(self, vacc_id, amountToReduce):    
        self._conn.execute("""
                UPDATE vaccines SET quantity=(quantity-(?)) WHERE id = ? 
        """, [amountToReduce, vacc_id])
    
    
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
        return c.fetchone()


    def findByName(self, sup_name):
        c = self._conn.cursor()
        c.execute("""
                SELECT * FROM suppliers WHERE name = ?
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

    def findByLocation(self, clinic_location):
        c = self._conn.cursor()
        c.execute("""
                SELECT * FROM clinics WHERE location = ?
            """, [clinic_location])    
        return c.fetchone()

    def updateDemand(self, clinic_id, amount):
        self._conn.execute("""
               UPDATE clinics SET demand=(demand-(?)) WHERE clinics.id=(?)
           """, [amount, clinic_id])

      
      
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

    def findByID(self, logistic_id):
        c = self._conn.cursor()
        c.execute("""
                SELECT * FROM logistics WHERE id = ?
            """, [logistic_id])
        return c.fetchone()

    def updateReceivedCount(self, logistic_id, amount):
        self._conn.execute("""
               UPDATE logistics SET count_received=(count_received+(?)) WHERE logistics.id=(?)
           """, [amount, logistic_id])

    def updateSentCount(self, logistic_id, supplied):
        self._conn.execute("""
               UPDATE logistics SET count_sent=(count_sent+(?)) WHERE logistics.id=(?)
           """, [supplied, logistic_id])