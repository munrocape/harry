"""
 _                _____ _                
| |              / __  (_)               
| |__   __ _ _ __`' / /'_ _ __ ___ __  __
| '_ \ / _` | '__| / / | | '_ ` _ \\ \/ /
| | | | (_| | |  ./ /__| | | | | | |>  < 
|_| |_|\__,_|_|  \_____/ |_| |_| |_/_/\_\\
                      _/ |
                     |__/ 

har2jmx converts an HTTP Archive into a JMeter Test Plan.
View the project at https://github.com/munrocape/har2jmx

Usage:
 har2jmx (-i <in> | --input <in>) [-o <out> | --output <out>] [-w | --waterfall] [-v | --verbose]
 har2jmx (-h | --help)
 har2jmx --version

Arguments:
 <in>       The path to the HTTP Archive.
 <out>        The name of the created JMeter Test Plan.

Options:
 -i  <in>, --input <in>               Filepath of HTTP Application to convert.
 -o <out>, --output <out>             Filename of created JMeter Test Plan.
 -w, --waterfall                      UNSUPPORTED. Emulate browser parsing of HTML, JS, CSS.
 -v, --verbose                        Verbosely list Page and Request conversion.
 -h, --help                           Show this screen.
 --version                            Show version.

"""


from docopt import docopt
from harpy.harpy.har import Har
import jinja2 

def _verbose_print(message):
	print message


def main():
	if(arguments['-i'] or arguments['--input']):
		input_file = arguments['<in>']
		verbose_print('Attempting to convert input file: ' + input_file + '\n')
		har = None
		
		try:
			har = Har(input_file)
		except IOError as e: # couldn't find the file
			print 'ERROR:'
			print input_file + ' is not a valid file.'
		except ValueError as e: # is not a JSON file
			print 'ERROR:'
			print input_file + ' is not a JSON file.'
		except KeyError as e: # does not conform to HTTP Archive specifications
			print 'ERROR:'
			print input_file + ' does not conform to the HTTP Archive standard.'
			print 'It is missing the following key: ' + str(e).strip('\'')


	else:
		print __doc__


if __name__ == '__main__':
	arguments = docopt(__doc__, version='har2jmx 0.0.1')
	if  arguments['--verbose'] or arguments['-v']:
		verbose_print = _verbose_print
	else:
		verbose_print = lambda *x: None
	main()
