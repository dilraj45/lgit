import requests
from retrying import retry
import re
import bs4


def set_header():
    hdr = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0)'
           ' Gecko/20100101 Firefox/21.0',
           'Accept':  'text/html,application/xhtml+xml,application/xml;'
           'q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1, utf-8; q=0.7,*; q=0.3',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'en-US,en;q=0.8'}
    return hdr


@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
def wait_for_connection():
    test = requests.get('http://216.58.197.46', timeout=2)
    test.raise_for_status()
    return


@retry(stop_max_attempt_number=5, wait_random_min=5000, wait_random_max=10000)
def get_html_text(url):
    hdr = set_header()
    try:
        htmlfile = requests.get(url, headers=hdr)
        htmlfile.raise_for_status()
    except requests.exceptions.SSLError:
        # check for https
        if url[4] == 's':
            url = url[0:4] + url[5:]
            raise
        else:
            htmlfile = requests.get(url, header=hdr, verify=False)
            htmlfile.raise_for_status()
    except requests.exceptions.ConnectionError:
        # checking for bad connection
        print "Waiting for Connection"
        wait_for_connection()
        raise
    return htmlfile.text


def get_list_id():
    return ['9332549443', '000100039X']


if __name__ == '__main__':
    id_list = get_list_id()
    fp = open('Priyam.csv', 'w+')
    fp.write(
        'ID;Book Name;5 star;4 star;3 star;2 star;1 star;'
        'Total Customer Reviews;Path\n')
    for i in id_list:
        link = 'http://amazon.in/dp/' + i
        soup = bs4.BeautifulSoup(get_html_text(link), 'lxml')
        # writing id to file
        fp.write(i + ';')

        # fetching book name
        name = soup.find('span', {'id': 'productTitle'}).string.encode('utf-8')
        fp.write(name + ';')

        # fetching total number of customer reviews and ratings
        total_reviews = 0
        table_ratings = soup.find('table', {'id': 'histogramTable'})
        for ratings in table_ratings.find_all('tr'):
            t = ratings.find_all('td', {'class': 'a-nowrap'})[1]
            s = re.sub(r'[^a-zA-Z0-9@ ]', r'', t.get_text().encode('utf-8'))
            total_reviews = total_reviews + int(s)
            fp.write(s + ';')
        fp.write(str(total_reviews) + ';')

        # fetching path
        container = soup.find(
            'div', {'id': 'wayfinding-breadcrumbs_container'})
        path = re.sub(r'[^\x00-\x7F]+', '/',
                      container.get_text().encode('utf-8'))
        path = re.sub(r'[^a-zA-Z/]', r'', path)
        print path
        fp.write(path + '\n')
    fp.close()
