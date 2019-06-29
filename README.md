Patch JUnit
===========

Update the statuses of junit xml files. 

Why?
----

Our application produces a junit file to record the results of its run. 
In order to show assertions can produce failures (i.e. they can assert) there are a bunch
of tests which produce failures in the xml file.

In a CI pipeline this will mark the build as a failure, which is correct but has no quantity to it. 
If test which are meant to pass fail or less test than expected fail this only shows up by looking at
the build stats and with a more obvious build starting to fail.

Enter _Patch JUnit._ Given the details of which tests are meant to fail it can read the junit xml file,
identify those tests and, if they have failed, mark them as passed, or if they have passed,
mark them as failed. Any other failing tests are left as failed. 

The end result is that only the expected tests fail then the resulting xml file will be fully passed,
and the CI build will be marked as success. On the other hand, if there are unexpected results, they
will cause the CI to fail and that should be a nice obvious alert.


