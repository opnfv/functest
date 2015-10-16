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
    main.getdefaultpara()

    #scripts to run
    runhandle = main.onosstart()
    main.RunScript(runhandle, "FUNCvirNetNB")
    main.RunScript(runhandle, "FUNCovsdbtest")
    main.onosclean( runhandle )
