#!/bin/bash
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Code structure is taken from [0] and changed according to
# functest unit test strategy.
# [0] https://github.com/openstack/rally/blob/
#     3f1e755e58aeb1712d3df826d61e099994f838ce/tests/ci/cover.sh
#

ALLOWED_EXTRA_MISSING=10

show_diff () {
    head -1 $1
    diff -U 0 $1 $2 | sed 1,2d
}

# Checkout master and save coverage report
git checkout HEAD^

baseline_report=$(mktemp -t functest_coverageXXXXXXX)
./run_unit_tests.sh > $baseline_report
line=$(awk '{ print $4}' $baseline_report) # Getting the last column of every line
lperc=$(echo $line | rev | cut -d' ' -f2 | rev) # cutting out final coverage percentage
baseline_missing=$(echo $lperc | rev | cut -d% -f2 | rev) # getting the integer from %


# Checkout back and save coverage report
git checkout -

current_report=$(mktemp -t functest_coverageXXXXXXX)
./run_unit_tests.sh > $current_report
line=$(awk '{ print $4}' $current_report)
lperc=$(echo $line | rev | cut -d' ' -f2 | rev)
current_missing=$(echo $lperc | rev | cut -d% -f2 | rev)


# Show coverage details
allowed_missing=$((baseline_missing+ALLOWED_EXTRA_MISSING))

echo "Allowed to introduce missing lines : ${ALLOWED_EXTRA_MISSING}"
echo "Missing lines in master            : ${baseline_missing}"
echo "Missing lines in proposed change   : ${current_missing}"

if [ $allowed_missing -gt $current_missing ];
then
    if [ $baseline_missing -lt $current_missing ];
    then
        show_diff $baseline_report $current_report
        echo "I believe you can cover all your code with 100% coverage!"
    else
        echo "Thank you! You are awesome! Keep writing unit tests! :)"
    fi
    exit_code=0
else
    show_diff $baseline_report $current_report
    echo "Please write more unit tests, we should keep our test coverage :( "
    exit_code=1
fi

rm $baseline_report $current_report
exit $exit_code
