import argparse
import os
import re
import sys
import time
import urllib.error
from random import randint
from random import shuffle

import googlesearch as gsearch
import pandas as pd
import requests
from colorama import init


def kill_cookie():
    """
    Removes generated google cookie file
    """
    if os.path.exists('.google-cookie'):
        os.remove('.google-cookie')


def message(msg, title=False, stat=False, word=False, banner=False):
    """
    Prints formatted text to CLI
    """

    class Colors:
        BLUE = '\033[94m'
        GREEN = "\033[32m"
        YELLOW = '\033[93m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'

    banner_text = """  ██████  ██▓ ▄████▄   ██ ▄█▀ ███▄    █ ▓█████  ██▀███  ▓█████▄ 
▒██    ▒ ▓██▒▒██▀ ▀█   ██▄█▒  ██ ▀█   █ ▓█   ▀ ▓██ ▒ ██▒▒██▀ ██▌
░ ▓██▄   ▒██▒▒▓█    ▄ ▓███▄░ ▓██  ▀█ ██▒▒███   ▓██ ░▄█ ▒░██   █▌
  ▒   ██▒░██░▒▓▓▄ ▄██▒▓██ █▄ ▓██▒  ▐▌██▒▒▓█  ▄ ▒██▀▀█▄  ░▓█▄   ▌
▒██████▒▒░██░▒ ▓███▀ ░▒██▒ █▄▒██░   ▓██░░▒████▒░██▓ ▒██▒░▒████▓ 
▒ ▒▓▒ ▒ ░░▓  ░ ░▒ ▒  ░▒ ▒▒ ▓▒░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░ ▒▒▓  ▒ 
░ ░▒  ░ ░ ▒ ░  ░  ▒   ░ ░▒ ▒░░ ░░   ░ ▒░ ░ ░  ░  ░▒ ░ ▒░ ░ ▒  ▒ 
░  ░  ░   ▒ ░░        ░ ░░ ░    ░   ░ ░    ░     ░░   ░  ░ ░  ░ 
      ░   ░  ░ ░      ░  ░            ░    ░  ░   ░        ░    
             ░                                           ░ """

    if title:
        print(f'{Colors.GREEN}{Colors.BOLD}[*] {msg}{Colors.ENDC}')
    elif stat:
        print(f'{Colors.BLUE}{msg}{Colors.ENDC}')
    elif word:
        return f'{Colors.YELLOW}{Colors.BOLD}{msg}{Colors.ENDC}{Colors.BLUE}'
    elif banner:
        print(f'{Colors.YELLOW}{banner_text}{Colors.ENDC}')


class SickNerd:
    def __init__(self, hosts_df, dorks_lst, do_validate=True):
        self.df = hosts_df
        self.df.drop_duplicates(subset=['HOSTNAME'], inplace=True)
        self.output_df = pd.DataFrame(columns=['QUERY', 'URL'])
        self.validate_bool = do_validate
        if dorks_lst:
            self.dorks_lst = dorks_lst
        else:
            self.dorks_lst = ['filetype:doc', 'filetype:docx', 'filetype:odp', 'filetype:ods', 'filetype:ott',
                              'filetype:rtf', 'filetype:txt', 'filetype:ppt', 'filetype:pptx', 'filetype:csv',
                              'filetype:pdf', 'filetype:xls', 'filetype:xlsx', 'filetype:7z', 'filetype:bz2',
                              'filetype:gz', 'filetype:rar', 'filetype:sql', 'filetype:sql.7z', 'filetype:sql.bz2',
                              'filetype:sql.gz', 'filetype:sql.rar', 'filetype:sql.sql', 'filetype:sql.tar',
                              'filetype:sql.tar.bz2',
                              'filetype:sql.tar.bzip2', 'filetype:sql.tar.gz', 'filetype:sql.tar.gzip',
                              'filetype:sql.tgz', 'filetype:sql.zip',
                              'filetype:sqlite', 'filetype:tar', 'filetype:tar.bz2', 'filetype:tar.bzip2',
                              'filetype:tar.gz', 'filetype:tar.gzip', 'filetype:tgz', 'filetype:zip', 'filetype:bat',
                              'filetype:key', 'filetype:env', 'filetype:log', 'filetype:reg', 'filetype:ini',
                              'filetype:yaml', 'filetype:swagger', 'filetype:mail', 'filetype:eml', 'filetype:mbox',
                              'filetype:mbx', 'filetype:csr', 'filetype:config']

    def start_query(self):
        """
        Starts searching the dorks
        :return: none
        """
        message('Starting file searches...', title=True)
        shuffle(self.dorks_lst)
        for d in self.dorks_lst:
            for h in self.df['HOSTNAME']:
                tld_str = self.df.HOSTNAME.str.split('.').iloc[0][1]
                site_str = f'site:{str(h)} '
                # checks if it has been queried already
                if self.output_df.loc[self.output_df['QUERY'].str.fullmatch(site_str, case=False)].shape[0] == 0:
                    self.search(site_str + str(d), tld_str)
            self.write_output()

        if self.validate_bool:
            message('Validating results...', title=True)
            valid_df = pd.DataFrame(self.output_df['URL'].apply(lambda x: self.validate(x)).tolist(),
                                    columns=['HTTP CODE', 'TITLE', 'CONTENT LENGTH'])
            self.output_df = pd.concat([self.output_df, valid_df], axis=1)
        self.write_output(final=True)

    def write_output(self, final=False):
        """
        Writes output df to csv file
        :param final: bool if final output
        :return: none
        """
        self.output_df.to_csv('s1cknerd-output.csv', index=False)
        if final:
            message(f'Writing {message(str(self.output_df.shape[0]), word=True)} results to file', stat=True)
            self.output_df.to_csv(os.path.join(args.output, 's1cknerd-output.csv'), index=False)

    def search(self, search_str, tld_str):
        """
        Searches via the google api. If 429 sleep then recall recursively.
        :param search_str: string to search
        :param tld_str: string of tld
        :return: none, appends to df
        """
        kill_cookie()
        ua_str = gsearch.get_random_user_agent().decode("utf-8")
        wait_int = randint(5, 10)
        count = 0
        try:
            for i in gsearch.search(str(search_str), tld=str(tld_str), num=10, stop=30, pause=wait_int,
                                    user_agent=ua_str):
                self.output_df.loc[self.output_df.shape[0]] = [search_str, str(i)]
                count += 1
            message(f'Found {message(str(count), word=True)} results from {message(search_str, word=True)}', stat=True)
        except urllib.error.HTTPError:
            message('Got 429 while searching! Sleeping!', title=True)
            time.sleep(randint(30, 60))
            self.search(search_str, tld_str)

    def validate(self, url):
        """
        Requests url and returns information. If 429 recursively calls again.
        :param url: str
        :return: list containing status code, title, and content-length
        """
        ua_str = gsearch.get_random_user_agent().decode("utf-8")
        try:
            resp = requests.get(str(url), headers={'User-Agent': str(ua_str)})
        except requests.exceptions.ConnectionError:
            return ['ERROR', 'ERROR', 'ERROR']

        if resp.status_code == 429:
            message('Got 429 while validating! Sleeping!', title=True)
            time.sleep(randint(30, 60))
            return self.validate(url)
        else:
            try:
                title = re.search('<\W*title\W*(.*)</title', resp.text, re.IGNORECASE).group(1)
            except AttributeError:
                title = 'NONE'
            return [resp.status_code, str(title), resp.headers['Content-length']]


if __name__ == '__main__':
    # colorama
    init()
    parser = argparse.ArgumentParser(description='CLI tool for making Google Dorking a passive recon experience')
    parser.add_argument("-i", "--input", action="store", default=False, help='Input list of domains (no subdomains).')
    parser.add_argument("-o", "--output", action="store", default=os.getcwd(),
                        help="Prints CSV files to directory. The default is cwd.")
    parser.add_argument("-d", "--dorks", action="store", default=[],
                        help="List of Dorks to test (optional)")
    parser.add_argument("-p", "--passive", action="store_false", default=True,
                        help="Skip the validation requests and only do passive checks.")
    parser.add_argument("-q", "--quiet", action="store_true", default=False,
                        help="Hides banner")
    args = parser.parse_args()

    if args.output:
        if args.output == '-':
            args.output = os.getcwd()

    if args.dorks:
        args.dorks = open(args.dorks, "r").read().split('\n')

    if not sys.stdin.isatty() and not args.input:
        args.input = sys.stdin

    try:
        if not args.quiet:
            message('', banner=True)
        df = pd.read_table(args.input, header=None, names=['HOSTNAME'], on_bad_lines='skip')
        df['HOSTNAME'] = df['HOSTNAME'].astype(str)
    except FileNotFoundError:
        print('No input file found')
        exit()

    dorker = SickNerd(df, args.dorks, args.passive)

    try:
        dorker.start_query()
        kill_cookie()
    except KeyboardInterrupt:
        message('CTRL + C pressed! Writing output then ending...', title=True)
        kill_cookie()
        dorker.write_output(final=True)
        exit()
