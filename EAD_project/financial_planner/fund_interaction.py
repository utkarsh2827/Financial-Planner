from requests_html import *
def get_mf_list():
    session = HTMLSession()
    r = session.get('https://www.morningstar.in/silver-rated-mutual-fund.aspx')
    var = r.html.find('.fundsArchive',first = True).html
    return var
