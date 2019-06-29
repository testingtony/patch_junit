#!/usr/bin/env python3

import xml.etree.ElementTree as ET

tree = ET.parse("junit_STS1.xml")

root = tree.getroot()

for suite in root.findall("testsuite"):
    root.remove(suite)
    for test_case in suite.findall("testcase"):
        if test_case.attrib['status'] == 'PASSED':
            suite.remove(test_case)
    if len(suite) > 0:
        del(suite.attrib['id'])
        del(suite.attrib['errors'])
        del(suite.attrib['failures'])
        del(suite.attrib['tests'])
        root.append(suite)

print(ET.tostring(root, encoding='UTF-8').decode('UTF-8'))


