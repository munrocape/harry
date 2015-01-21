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
 <out>      The name of the created JMeter Test Plan.

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
from harry_help import generate_test_plan, _verbose_print


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
		if har != None:
			output_file = 'test_plan.jmx'
			generate_test_plan(har, output_file)
	else:
		print __doc__


if __name__ == '__main__':
	arguments = docopt(__doc__, version='harry 0.0.1')
	print arguments
	if  arguments['--verbose'] or arguments['-v']:
		verbose_print = _verbose_print
	else:
		verbose_print = lambda *x: None
	main()
