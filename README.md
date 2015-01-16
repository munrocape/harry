#har2jmx 

har2jmx is a command line utility that will convert a HTTP Archive (har) into a JMeter test plan (jmx)

###Why?
HTTP Archives are great for recording all of the requests made on a page. However, a typical webpage will have dozens of such requests. To accurately test the performance of a webpage with JMeter, you would need to manually replicate the requests. 

This reads in a HTTP Archive, spanning one or multiple pages, and generates a JMeter test plan to replicate the requests. This can then be directly used by JMeter to begin testing.
