"""
Description: This test is to run onos Teston VTN scripts

List of test cases:
CASE1 - Northbound NBI test network/subnet/ports
CASE2 - Ovsdb test&Default configuration&Vm go online

lanqinglong@huawei.com
"""
from adapters.client import client


if __name__=="__main__":
    
    
    main = client()
    main.masterusername = "root"
    main.masterpassword = "root"
    main.agentusername = "root"
    main.agentpassword = "root"
    main.OCT = '189.42.8.99'
    main.OC1 = '189.42.8.101'
    main.OC2 = '189.42.8.102'
    main.OC3 = '189.42.8.103'
    main.OCN = '189.42.8.104'
    main.OCN2 = '189.42.8.105'
    main.localhost = main.OCT
    main.onosbasic()
    
    #scripts to run
    main.RunScript("FUNCvirNetNB")
    main.RunScript("FUNCovsdbtest")
