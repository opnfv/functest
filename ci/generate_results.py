import json
import urllib2
import requests


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
            stop_date = test['stop_date']
            # duration = int(stop_date) - int(start_date)

            if criteria != 'unknown':
                url = 'http://testresults.opnfv.org/test/api/v1/results?id=' + \
                    id

    return {'id': id,
            'testname': testname,
            'criteria': criteria,
            'start_date': start_date,
            'stop_date': stop_date,
            'duration': duration,
            'url': url
            }


def main(args):

    test_2_report = []

    build_tag = 'jenkins-functest-fuel-baremetal-daily-master-999'
    url = 'http://testresults.opnfv.org/test/api/v1/results?build_tag=' + \
        build_tag
    data = json.load(urllib2.urlopen(url))
    results = data['results']
    # print len(results)
    # for result in results:
    #    print result['case_name']

    tiers = args
    for tier in tiers:
        for test in tier.get_tests():
            testname = test.get_name()
            test_2_report.append(get_data(results, testname))

    print test_2_report

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
