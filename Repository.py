#The Repository
import DAO
import DTO
import sqlite3
import atexit
from datetime import datetime
  
class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.vaccines = DAO._Vaccines(self._conn)
        self.suppliers = DAO._Suppliers(self._conn)
        self.clinics = DAO._Clinics(self._conn)
        self.logistics = DAO._Logistics(self._conn)    

    def _close(self):
        self._conn.commit()
        self._conn.close()
    
    def create_tables(self):
        self._conn.executescript("""        
        CREATE TABLE IF NOT EXISTS vaccines (
            id INTEGER PRIMARY KEY,
            date DATE NOT NULL,
            supplier INTEGER REFERENCES suppliers(id),
            quantity INTEGER NOT NULL
        );
    
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY,
            name STRING NOT NULL,
            logistic INTEGER REFERENCES logistics(id)
        );
    
        CREATE TABLE IF NOT EXISTS clinics (
            id INTEGER PRIMARY KEY,
            location STRING NOT NULL,
            demand INTEGER NOT NULL,
            logistic INTEGER REFERENCES logistics(id)
        );

        CREATE TABLE IF NOT EXISTS logistics (
            id INTEGER PRIMARY KEY,
            name STRING NOT NULL,
            count_sent INTEGER NOT NULL,
            count_received INTEGER NOT NULL
        );
        """)
    
    def receive_shipment(self, arrOfCurrOrder):
        supplier_id = self.suppliers.findByName(arrOfCurrOrder[0])[0]        
        vaccToAdd = DTO.Vaccine(arrOfCurrOrder[2], supplier_id, arrOfCurrOrder[1])
        self.vaccines.insert(vaccToAdd)
        self._conn.commit()

# the repository singleton
repo = _Repository()
atexit.register(repo._close)
