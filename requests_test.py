import requests

def infer_encoding(headers_content_type):
    if not isinstance(headers_content_type, str):
        raise TypeError("'headers_content_type' must be the original header['content-type'] string")

    content_type = headers_content_type.split(';')

    content_encoding = None

    for param in content_type:
        split_params = param.split('charset=')
        if len(split_params) == 2 and split_params[0] == '':
            content_encoding = split_params[1]
            break

    return(content_encoding)

def get_and_parse_json(url):
    query_request = requests.get(url)
    content_encoding = infer_encoding(query_request.headers['content-type'])

    if content_encoding is not None:
        query_request.encoding = content_encoding

    return(query_request.json())

oecd_base_url = 'http://stats.oecd.org/sdmx-json/data/'
oecd_url = oecd_base_url + 'QNA/AUS+AUT.GDP+B1_GE.CUR+VOBARSA.Q/all?startTime=2009-Q2&endTime=2011-Q4&dimensionAtObservation=allDimensions&detail=Full'
query_response = get_and_parse_json(oecd_url)
