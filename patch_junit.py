#!/usr/bin/env python3

import xml.etree.ElementTree as ET


def flip_results(expected, actual):
    for expected_suite in expected.findall("testsuite"):
        expected_suite_name = expected_suite.attrib['name']
        for expected_case in expected_suite.findall("testcase"):
            expected_case_name = expected_case.attrib['name']
            for actual_suite in actual.findall("./testsuite[@name='{}']".format(expected_suite_name)):
                for actual_case in actual_suite.findall("./testcase[@name='{}']".format(expected_case_name)):
                    if expected_case.attrib['status'] == actual_case.attrib['status']:
                        actual_case.attrib['status'] = 'PASSED'
                    else:
                        actual_case.attrib['status'] == 'FAILED'

        for actual_suite in actual.findall("testsuite"):
            failed = actual_suite.findall("./testcase[@status='FAILED']")
            actual_suite.attrib['failures'] = str(len(failed))

    failed_tests = actual.findall("./testsuite/testcase[@status='FAILED']")
    actual.attrib['failures'] = str(len(failed_tests))

    print(ET.tostring(actual, encoding='UTF-8').decode('UTF-8'))



def main(source_file_name, expected_file_name, destination_file_name):
    actual_tree = ET.parse(source_file_name)
    actual_root = actual_tree.getroot()

    expected_tree = ET.parse(expected_file_name)
    expected_root = expected_tree.getroot()

    flip_results(expected_root, actual_root)



if __name__ == '__main__':
    main("junit_STS1.xml", "expected.xml", "destination.xml")