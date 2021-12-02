 
import time
import requests
from bs4 import BeautifulSoup
import pytz
import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from nagiode.cmdtyp import CmdTyp, CommandArguments, ArgumentDefaults

class Nagios:
    def __init__(self, hostname, userid = None, password = None,
                 secure = True, cgi_path = '/nagios/cgi-bin', debug = False):

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        self.debug = debug
        self.author = userid
        self.password = password
        self.auth = (self.author, self.password)

        _s = ""
        if secure:
            _s = "s"

        self.base_uri = f"http{_s}://{hostname}{cgi_path}"

    def list_commands(self):
        return list(CommandArguments.keys())

    def list_arguments(self, command):
        return CommandArguments[command]

    def cmd(self, command, **kwargs):
        cmd = getattr(CmdTyp, command)

        #kwargs['cmd_typ'] = cmd.value
        #kwargs['cmd_mod'] = 2

        params = {"cmd_typ": cmd.value}

        args = CommandArguments.get(cmd.name,[]) + ["cmd_mod"]
        for a in args:
            params[a] = kwargs.get(a, ArgumentDefaults.get(a, ""))

        if 'author' in params and not params['author']:
            params['author'] = self.author
        if 'com_author' in params and not params['com_author']:
            params['com_author'] = self.author

        if self.debug:
            print(f"URI: {self.base_uri}/cmd.cgi")
            print(f"DATA: {params}")
            return
            
        result = requests.get(f"{self.base_uri}/cmd.cgi", verify=False, params=params, auth=self.auth).text
            
        soup = BeautifulSoup(result, 'html.parser')

        msg = ""
            
        try:
            msg = soup.find('div', class_="infoMessage").get_text()
        except:
            pass

        if not msg:
            try:
                msg = soup.find('div', class_="errorMessage").get_text() #+ soup.find('div', class_="errorDescription").get_text()
            except:
                pass

        if not msg:
            msg = result

        return msg

    def status(self, host):
        """
        Parsing nagios is pretty awful. It puts a bunch of 
        unnecessary tables and stuff in everything. 
        """

        result = requests.get(f"{self.base_uri}/status.cgi", verify=False, params={"host": host}, auth=self.auth).text

        soup = BeautifulSoup(result, 'html.parser')

        cols = soup.find_all("td", class_="statusOdd") + soup.find_all("td", class_="statusEven")

        status = {}
        i=0
        while i < len(cols):
            if cols[i].get_text().strip() == host:
                i+=1
                continue

            if i+7 > len(cols):
                break

            name = cols[i].get_text().strip()
            last_check = cols[i+3].get_text().strip()
            duration = cols[i+4].get_text().strip()
            attempt = cols[i+5].get_text().strip()
            stat = cols[i+6].get_text().strip()

            status[name] = { "last_check": last_check, "duration": duration, "attempt": attempt, "status": stat }

            i+=7
        return status
