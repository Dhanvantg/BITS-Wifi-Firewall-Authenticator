import requests
import pathlib


headers = \
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}


def login(uname, passw, path):
    url_1 = 'http://www.msftconnecttest.com/redirect'
    session = requests.Session()
    res = session.get(url_1, headers=headers)
    url_2 = res.text.split('"')[3]
    magic = url_2.split('?')[1]
    payload = {
        '4Tredir': 'http://google.com/',
        'username': uname,
        'password': passw,
        'magic': str(magic),
    }
    res1 = session.get(url_2, headers=headers)
    res = requests.post(url_2, headers=headers, data=payload)
    # print res.text
    if 'Failed' in res.text:
        print('Authentication failed, Check credentials.txt')
        return False
    else:
        print(uname + ':' + passw)
        print(res.url)
        with open(path + '/magic.txt', 'w') as f:
            f.write(magic)
        return True


def main(username, password, path):

    ip_addr = "fw.bits-pilani.ac.in"
    port = "8090"

    print("Checking connectivity..")
    try:
        res = requests.head('http://www.google.co.in')
        print('Already connected. :)')

        with open('magic.txt') as f:
            magic = f.read()
        if magic == '':
            exit(0)

        requests.get(
            url='https://'+ip_addr+':'+port+'/logout?'+magic, headers=headers)
        print("Refreshing Authentication")

        if login(username, password, path):
            print("Authentication Refreshed")
    except requests.ConnectionError:

        
        if login(username, password, path):
            # r = get(
                # url="http://172.16.12.1:1000/logout?0c0a0e0a0a1fea52", headers=headers)
            print("Logged in")
            
            exit(0)
        else:
            pass


if __name__ == '__main__':
    path = str(pathlib.Path(__file__).parent.resolve())
    with open(path+"/credentials.txt") as f:
        username = f.readline().strip().upper()
        password = f.readline().strip().upper()
    print(username, password)
    main(username, password, path)