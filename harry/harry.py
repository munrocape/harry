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
from jinja2 import Environment, PackageLoader
import xml.dom.minidom
ENV = Environment(loader=PackageLoader('harry', 'templates'))


def _verbose_print(message):
    """Write message to STDOUT."""
    print message


def generate_test_plan(har, output='test_plan.jmx'):
    """Convert a HTTP Archive and write out a JMeter Test Plan."""
    test_plan_template = ENV.get_template('test_plan.xml')
    formatted_pages = []
    for page in har.pages:
        entries = har.entries_by_page_ref(page.id)
        formatted_pages.append(generate_page(page.id, entries))
    generated_test = test_plan_template.render(pages=formatted_pages)
    # format test
    formatted_xml = xml.dom.minidom.parseString(xml_fname) 
    pretty_xml = xml.toprettyxml()
    try:
        output_file = open(output, 'w')
        output_file.write(pretty_xml)
    except IOError:
        print 'ERROR:'
        print 'do not have permission to write to file.'
    else:
        print 'file created at ' + output


def generate_page(page_ref, entries):
    """Return a JMeter Controller as a string."""
    transaction_template = ENV.get_template('transaction.xml')
    formatted_entries = []
    for entry in entries:
        formatted_entries.append(generate_entry(entry))
    generated_page = transaction_template.render(page_name=page_ref,
                                                 requests=formatted_entries)
    return generated_page


def generate_entry(entry):
    """Given a HAR entry, it returns a JMeter formatted HTTP Request."""
    argument_template = ENV.get_template('argument.xml')
    post_template = ENV.get_template('post.xml')
    entry_template = ENV.get_template('request.xml')
    xml_request_template = ENV.get_template('xmlrequest.xml')
    formatted_arguments = []
    for argument in entry.request.query_string:
        arg_value = argument.value.replace('&', '&amp;')
        formatted_arguments.append(
            argument_template.render(
                argument_name=argument.name,
                argument_value=arg_value))

    url_dict = extract_url_information(entry.request.url)

    post = []
    request_end = '<hashTree/>'
    if entry.request.post_data:
        post = [post_template.render(post_text=entry.request.post_data['text']
                                                    .replace('&', '&amp;')
                                                    .replace('"', '&quot;'))]
        request_end = xml_request_template.render()
    generated_entry = entry_template.render(arguments=formatted_arguments,
                                            post_data=post,
                                            request_end=request_end,
                                            url=url_dict['url'],
                                            path=url_dict['path'],
                                            domain=url_dict['domain'],
                                            protocol=url_dict['protocol'],
                                           method=entry.request.method,
                                            port=443)
    return generated_entry


def extract_url_information(url):
    """Return a dictionary containing URL-specific information."""
    protocol = url[:url.index(':')].replace('&', '&amp;')
    post_protocol = url.index('//')
    post_domain = url.index('/', post_protocol + 2)
    domain = url[post_protocol + 2:post_domain]
    path = url[post_domain:].replace('&', '&amp;')
    return {'url': url.replace('&', '&amp;'),
            'path': path,
            'domain': domain,
            'protocol': protocol}


def main():
    """Convert HTTP Archive to JMeter Test Plan."""
    args = docopt(__doc__, version='harry 0.0.19')
    if args['--verbose'] or args['-v']:
        v_print = _verbose_print
    else:
        v_print = lambda *x: None
    if args['-i'] or args['--input']:
        input_file = args['<in>']
        v_print('Attempting to convert input file: ' + input_file + '\n')
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
    
    main()
