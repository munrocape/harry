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
  harry (-i <in> | --input <in>) [-o <out> | --output <out>]
                                 [-w | --waterfall]
                                 [-v | --verbose]
  harry (-h | --help)
  harry --version

ARGUMENTS:
  <in>       The path to the HTTP Archive.
  <out>      The name of the file that the JMeter script should be written to.

Options:
  -o  <out>, --output <out>  Filepath of HTTP Application to convert.
  -h, --help                 Show this screen.
  -w, --waterfall            UNSUPPORTED. Mimic browser parsing of CSS/HTML/JS.
  -v, --verbose              Output the pages and requests that are converted.
  --version                  Show version.

"""


from docopt import docopt
from harpy.harpy.har import Har
from harry_help import generate_test_plan, _verbose_print


def main():
    """Convert HTTP Archive to JMeter Test Plan."""
    if ARGUMENTS['-i'] or ARGUMENTS['--input']:
        input_file = ARGUMENTS['<in>']
        VERBOSE_PRINT('Attempting to convert input file: ' + input_file + '\n')
        har = None
        try:
            har = Har(input_file)
        except IOError:
            # Python couldn't find the file
            print 'ERROR:'
            print input_file + ' is not a valid file'
        except ValueError:
            # File is not a JSON file
            print 'ERROR:'
            print input_file + ' is not a JSON file'
        except KeyError as missing_key:
            # File does not conform to HTTP Archive specifications
            print 'ERROR:'
            print input_file + ' does not conform to the HTTP Archive standard'
            print 'Expected the following key: ' + str(missing_key).strip('\'')
        if har is not None:
            output_file = 'test_plan.jmx'
            generate_test_plan(har, output_file)
    else:
        print __doc__


if __name__ == '__main__':
    ARGUMENTS = docopt(__doc__, version='harry 0.0.1')
    if ARGUMENTS['--verbose'] or ARGUMENTS['-v']:
        VERBOSE_PRINT = _verbose_print
    else:
        VERBOSE_PRINT = lambda *x: None
    main()
