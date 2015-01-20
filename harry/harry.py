"""
                                                                                                      
 _                           
| |__   __ _ _ __ _ __ _   _ 
| '_ \ / _` | '__| '__| | | |
| | | | (_| | |  | |  | |_| |
|_| |_|\__,_|_|  |_|   \__, |
                       |___/ 

harry converts an HTTP Archive into a JMeter Test Plan.
View the project at https://github.com/munrocape/harry

Usage:
 harry (-i <in> | --input <in>) [-o <out> | --output <out>] [-w | --waterfall] [-v | --verbose]
 harry (-h | --help)
 harry --version

Arguments:
 <in>       The path to the HTTP Archive.
 <out>        The name of the created JMeter Test Plan.

Options:
 -i  <in>, --input <in>               Filepath of HTTP Application to convert.
 -o <out>, --output <out>             Filename of created JMeter Test Plan.
 -w, --waterfall                      UNSUPPORTED. Emulate browser parsing of HTML, JS, CSS.
 -v,  --verbose                       Verbosely list Page and Request conversion.
 -h, --help                           Show this screen.
 --version                            Show version.

"""


from docopt import docopt
from harpy.harpy.har import Har
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('harry', 'templates'))


def _verbose_print(message):
	print message


def generate_test_plan(har):
	'''Return a JMeter formatted test plan from a HTTP Archive.'''
	formatted_pages = []
	for p in har.pages:
		entries = har.entries_by_page_ref(p.id)
		formatted_pages.append(generate_page(p.id, entries))
	#print formatted_pages


def generate_page(page_ref, entries):
	'''Return a JMeter formatted Controller from a page_ref and its subsequent entries.'''
	template = env.get_template('transaction.xml')
	formatted_entries = []
	for entry in entries:
		formatted_entries.append(generate_entry(entry))
	return formatted_entries


def generate_entry(entry):
	''' Given a HAR entry, it returns a JMeter formatted HTTP Request.'''
	argument_template = env.get_template('argument.xml')
	entry_template = env.get_template('request.xml')
	formatted_arguments = []
	for argument in entry.request.query_string:
		formatted_arguments.append(argument_template.render(argument_name=argument.name, argument_value=argument.value))
	
	url_dict = extract_url_information(entry.request.url)
	print entry_template.render(arguments=formatted_arguments, \
								path = url_dict['path'], \
								domain = url_dict['domain'], \
								protocol = url_dict['protocol'], \
								method = entry.request.method, \
								port = 442)
	return []


def extract_url_information(url):
	'''Return a dictionary containing the protocol, domain, and path of a URL.'''
	protocol = url[:url.index(':')]
	post_protocol = url.index('//')
	post_domain = url.index('/', post_protocol + 2)
	domain = url[post_protocol + 2:post_domain]
	path = url[post_domain:]
	return {'path':path, 'domain':domain,'protocol':protocol}


def main():
	if(arguments['-i'] or arguments['--input']):
		input_file = arguments['<in>']
		verbose_print('Attempting to convert input file: ' + input_file + '\n')
		har = None
		
		try:
			har = Har(input_file)
		except IOError as e: # Python couldn't find the file
			print 'ERROR:'
			print input_file + ' is not a valid file.'
		except ValueError as e: # File is not a JSON file
			print 'ERROR:'
			print input_file + ' is not a JSON file.'
		except KeyError as e: # File does not conform to HTTP Archive specifications
			print 'ERROR:'
			print input_file + ' does not conform to the HTTP Archive standard.'
			print 'Expected the following key: ' + str(e).strip('\'')
		generate_test_plan(har)
	else:
		print __doc__


if __name__ == '__main__':
	arguments = docopt(__doc__, version='harry 0.0.1')
	if  arguments['--verbose'] or arguments['-v']:
		verbose_print = _verbose_print
	else:
		verbose_print = lambda *x: None
	main()
