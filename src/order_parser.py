from lxml import html

def parse_html_table(html_string):
    # Create an lxml HTML parser
    parser = html.HTMLParser()

    # Parse the HTML string
    tree = html.fromstring(html_string, parser=parser)

    # Find the table element in the HTML
    table = tree.xpath("//table")[0]

    # Extract the table headers
    headers = [th.text_content().strip() for th in table.xpath(".//th")]

    # Extract the table rows
    rows = []
    for tr in table.xpath(".//tr"):
        row = [td.text_content().strip() for td in tr.xpath(".//td")]
        if row:
            rows.append(row)

    # Return the headers and rows
    return headers, rows
