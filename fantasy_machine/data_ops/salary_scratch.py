def retrieve_past_salaries(years=None, weeks=None, site='fd'):
	import requests
	from lxml import html, etree

	base_url = 'http://rotoguru1.com/cgi-bin/fyday.pl?week={week}&year={year}&game={site}&scsv=1'

	if years == None:
		years = range(2011,2019)
	if weeks == None:
		weeks = range(1,18)

	for year in years:
		for week in weeks:
			page = requests.get(base_url.format(week=week, year=year, site=site))
			tree = html.fromstring(page.content)
			csv = tree.xpath("//pre/text()")
			try:
				len(final_csv)
				final_csv += csv
			except:
				final_csv = csv
	return final_csv