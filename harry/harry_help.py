from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('harry_help', 'templates'))


def _verbose_print(message):
	print message


def generate_test_plan(har, output='test_plan.jmx'):
	'''Return a JMeter formatted test plan from a HTTP Archive.'''
	test_plan_template = env.get_template('test_plan.xml')
	formatted_pages = []
	for p in har.pages:
		entries = har.entries_by_page_ref(p.id)
		formatted_pages.append(generate_page(p.id, entries))
	generated_test = test_plan_template.render(pages=formatted_pages)
	#generated_test = generated_test.replace('&', '&amp;')
	try:
		output_file = open(output, 'w')
		output_file.write(generated_test)
	except IOError:
		print 'ERROR:'
		print 'do not have permission to write to file.'
	else:
		print 'file created at ' + output


def generate_page(page_ref, entries):
	'''Return a JMeter formatted Controller from a page_ref and its subsequent entries.'''
	transaction_template = env.get_template('transaction.xml')
	formatted_entries = []
	for entry in entries:
		formatted_entries.append(generate_entry(entry))
	generated_page = transaction_template.render(page_name=page_ref, requests=formatted_entries)
	return generated_page


def generate_entry(entry):
	'''Given a HAR entry, it returns a JMeter formatted HTTP Request.'''
	argument_template = env.get_template('argument.xml')
	post_template = env.get_template('post.xml')
	entry_template = env.get_template('request.xml')
	xml_request_template = env.get_template('xmlrequest.xml')
	formatted_arguments = []
	for argument in entry.request.query_string:
		arg_value = argument.value.replace('&', '&amp;')
		formatted_arguments.append(argument_template.render(argument_name=argument.name, argument_value=arg_value))
	url_dict = extract_url_information(entry.request.url)

	post = []
	request_end = '<hashTree/>'
	if entry.request.post_data:
		post = [post_template.render(post_text=entry.request.post_data['text'].replace('&','&amp;').replace('"', '&quot;'))]
		request_end = xml_request_template.render()
	generated_entry = entry_template.render(arguments=formatted_arguments, \
											post_data = post, \
											request_end = request_end, \
								url = url_dict['url'], \
								path = url_dict['path'], \
								domain = url_dict['domain'], \
								protocol = url_dict['protocol'], \
								method = entry.request.method, \
								port = 443)
	return generated_entry


def extract_url_information(url):
	'''Return a dictionary containing the protocol, domain, and path of a URL.'''
	protocol = url[:url.index(':')].replace('&', '&amp;')
	post_protocol = url.index('//')
	post_domain = url.index('/', post_protocol + 2)
	domain = url[post_protocol + 2:post_domain]
	path = url[post_domain:].replace('&', '&amp;')
	return {'url':url.replace('&', '&amp;'), 'path':path, 'domain':domain, 'protocol':protocol}
