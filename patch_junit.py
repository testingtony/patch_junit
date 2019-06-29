#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import copy


def flip_results(expected, actual):
    for expected_suite in expected.findall("testsuite"):
        expected_suite_name = expected_suite.attrib['name']
        for expected_case in expected_suite.findall("testcase"):
            expected_case_name = expected_case.attrib['name']
            for actual_suite in actual.findall("./testsuite[@name='{}']".format(expected_suite_name)):
                for actual_case in actual_suite.findall("./testcase[@name='{}']".format(expected_case_name)):
                    if expected_case.attrib['status'] == actual_case.attrib['status']:
                        actual_case.attrib['status'] = 'PASSED'
                        for failure_message in actual_case.findall('failure'):
                            actual_case.remove(failure_message)
                            actual_case.text = None
                    else:
                        new_case = copy.deepcopy(expected_case)
                        new_case.attrib['status'] = 'FAILED'
                        actual_suite.remove(actual_case)
                        actual_suite.append(new_case)

        for actual_suite in actual.findall("testsuite"):
            failed = actual_suite.findall("./testcase[@status='FAILED']")
            actual_suite.attrib['failures'] = str(len(failed))

    failed_tests = actual.findall("./testsuite/testcase[@status='FAILED']")
    actual.attrib['failures'] = str(len(failed_tests))


def main(source, expected, destination):
    actual_tree = ET.parse(source)
    actual_root = actual_tree.getroot()

    expected_tree = ET.parse(expected)
    expected_root = expected_tree.getroot()

    flip_results(expected_root, actual_root)

    destination.write(ET.tostring(actual_root, encoding='UTF-8').decode('UTF-8'))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Change the results in a JUnit file')
    parser.add_argument('original_file', type=argparse.FileType("r"))
    parser.add_argument('expected_file', type=argparse.FileType("r"))
    parser.add_argument('destination_file', type=argparse.FileType("w"), default='-', nargs='?')

    args = parser.parse_args()
    main(args.original_file, args.expected_file, args.destination_file)

    args.destination_file.close()
