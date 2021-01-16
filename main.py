import csv
import sqlite3
import sys
import DTO
from Repository import repo
import os
import imp
 
def main():
    init_tables(sys.argv[1]) 
    init_order(sys.argv[2])
    sys.exit()

def init_tables(config_dir):
    repo.create_tables()
    dirs = open(config_dir, "r")
    entities = dirs.readline()
    arrOfEntities = entities.split(',')
    numOFVaccines = int(arrOfEntities[0])
    numOfSuppliers = int(arrOfEntities[1])
    numOfClinics = int(arrOfEntities[2])
    numOfLogistics = int(arrOfEntities[3])    
    for x in range(numOFVaccines):
        currLine = dirs.readline()
        arrCurrVacc = currLine.split(',')
        currVacc = DTO.Vaccine(0, arrCurrVacc[1], arrCurrVacc[2], arrCurrVacc[3])
        repo.vaccines.insert(currVacc)         
    
    for x in range(numOfSuppliers):
        currLine = dirs.readline()
        arrCurrSupp = currLine.split(',')
        currSupp = DTO.Supplier(arrCurrSupp[0], arrCurrSupp[1], arrCurrSupp[2])
        repo.suppliers.insert(currSupp) 

    for x in range(numOfClinics):
        currLine = dirs.readline()
        arrCurrClin = currLine.split(',')
        currClin = DTO.Clinic(arrCurrClin[0], arrCurrClin[1], arrCurrClin[2], arrCurrClin[3])
        repo.clinics.insert(currClin) 

    for x in range(numOfLogistics):
        currLine = dirs.readline()
        arrCurrLogs = currLine.split(',')
        currLogs = DTO.Logistic(arrCurrLogs[0], arrCurrLogs[1], arrCurrLogs[2], arrCurrLogs[3])
        repo.logistics.insert(currLogs) 
        
    repo._conn.commit()
    dirs.close()

def init_order(order_dir):    
    dirs = open(order_dir, "r")
    for row in dirs:
        arrCurrOrder = row.split(',')
        length = len(arrCurrOrder)
        if length == 3:
            repo.receive_shipment(arrCurrOrder)
        if length == 2:
            repo.send_shipment(arrCurrOrder)
        updateOutput()

def updateOutput():
    outputLine = [repo.vaccines.totalInventory()[0], repo.clinics.totalDemand()[0], repo.logistics.totalReceived()[0], repo.logistics.totalSent()[0]]
    dirs = open(sys.argv[3], "a")
    toWrite = ','.join(map(str, outputLine))
    dirs.write(toWrite + '\n')
    dirs.close()

if __name__== '__main__':
    main()