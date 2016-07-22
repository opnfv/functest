import json
import urllib2
import requests
import os
from datetime import datetime

def get_data(results, testname):
    criteria = 'unknown'
    start_date = 0
    stop_date = 0
    duration = 0
    url = ''
    id = ''
    for test in results:
        if test['case_name'] == testname:
            id = test['_id']
            criteria = test['criteria']
            start_date = test['start_date']
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
            stop_date = test['stop_date']
            stop_date_obj = datetime.strptime(stop_date, '%Y-%m-%d %H:%M:%S')
            seconds = (stop_date_obj - start_date_obj).seconds
            duration = ("%02d:%02d" % divmod(duration, 60))
            
            if id != '':
                url = 'http://testresults.opnfv.org/test/api/v1/results/' + id

    return {'id': id,
            'test_name': testname,
            'result': criteria,
            'duration': duration,
            'url': url
            }


def main(args):

    test_2_report = []

    build_tag = os.getenv("BUILD_TAG")
    url = 'http://testresults.opnfv.org/test/api/v1/results?build_tag=' + \
        build_tag
    data = json.load(urllib2.urlopen(url))
    results = data['results']
    # print len(results)
    # for result in results:
    #    print result['case_name']
    tiers = args[0]
    executed_test_cases = args[1]
    
    
    for tier in tiers:
        for test in tier.get_tests():
            testname = test.get_name()
            data = get_data(results, testname, testname)
            test_2_report.append()

    print test_2_report

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
