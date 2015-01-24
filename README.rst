harry
=====

harry is a command line utility that will convert a HTTP Archive (har)
into a JMeter test plan (jmx)

Why?
~~~~

JMeter is a tool used to test the reponses for a given HTTP request.
However, a typical webpage is comprised of dozens of such requests. To
accurately test the performance of a webpage with JMeter, you would need
to perform a great deal of manual entry.

HTTP Archives are great for recording all of the requests made on a page
- exactly the data one would need to replicate all the requests for a
JMeter test.

This reads in a HTTP Archive, spanning one or multiple pages, and
generates a JMeter test plan to replicate the requests. This can then be
directly used by JMeter to begin testing.
