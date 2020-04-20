import requests
import bs4
import urllib.parse
import uuid
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import json
from testapi.settings import BASE_DIR
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class AccessToken():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        capabilities = DesiredCapabilities.CHROME
        capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
        self.session = requests.Session()
        self.driver = webdriver.Chrome(executable_path=os.path.abspath(BASE_DIR+"/driver/chromedriver" ),chrome_options=chrome_options,desired_capabilities=capabilities)

    def extract_basic_token(self, email, passwd):
        self.driver.get("https://admin.webex.com/")
        time.sleep(1)
        self.driver.find_element_by_xpath("//input[@type='email']").send_keys(email)
        time.sleep(1)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(4)
        self.driver.find_element_by_xpath("//input[@type='password']").send_keys(passwd)
        time.sleep(1)
        self.driver.find_element_by_xpath("//button[@id='Button1']").click()
        self.driver.implicitly_wait(20)
        time.sleep(3)
        auth = ""
        for entry in self.driver.get_log('performance'):
            try:
                print(entry)
                if "Basic" in json.loads(entry['message'])['message']['params']['request']['headers']['Authorization']:
                    auth = json.loads(entry['message'])['message']['params']['request']['headers']['Authorization']
                    print(auth)
                    self.driver.close()
                    return auth

            except:
                pass
        self.driver.close()
        return auth
    def convert_ids_and_secret(self,basic):
        user_info = {}
        convert =  base64.b64decode(basic.split(' ')[1]).decode('UTF-8').split(':')
        user_info['client_id'] = convert[0]
        user_info['secret_key'] = convert[1]
        return user_info

    def token(self,email, passwd):

        basic = self.extract_basic_token(email,passwd)
        user =  self.convert_ids_and_secret(basic)
        access_token = self.access_token(user,email,passwd)


        return access_token
    def access_token(self, user,em,passwd):

        scope = 'atlas-order:create_user webexsquare:admin webexsquare:billing ciscouc:admin Identity:SCIM Identity:Config Identity:Organization Identity:OAuthToken Identity:authz_token cloudMeetings:login webex-messenger:get_webextoken cloud-contact-center:admin spark-compliance:rooms_read spark-compliance:people_read spark-compliance:organizations_read spark-compliance:ediscovery_report compliance:spark_conversations_read contact-center-context:pod_read contact-center-context:pod_write spark-admin:people_read spark-admin:people_write spark-admin:customers_read spark-admin:customers_write spark-admin:organizations_read spark-admin:licenses_read spark-admin:logs_read spark-admin:policies_read spark-admin:policies_write spark:kms spark:applications_write spark:applications_read spark:people_read spark:messages_read spark:memberships_read spark:memberships_write spark:rooms_read spark:xapi_commands ucmgmt-uaas:admin ucmgmt-laas:admin cjp:organization spark-admin:cpapi_rw ucmgmt:admin'
        state = str(uuid.uuid4())
        redirect_uri = 'https://admin.webex.com/'
        data = {
            'response_type': 'code',
            'state': state,
            'client_id': user['client_id'],
            'redirect_uri': redirect_uri,
            'scope': scope
        }

        response = self.session.get("https://idbroker.webex.com/idb/oauth2/v1/authorize", params=data)
        soup = bs4.BeautifulSoup(response.text, 'html5lib')
        title = soup.find('title')

        form_title = title.text.strip()
        form = soup.find(id='GlobalEmailLookupForm')
        inputs = form.find_all('input')
        inputs[0]['value'] = 'aliumam000+webex@gmail.com'
        form_data = {i['name']: i['value'] for i in inputs}
        form_action = self.form_action_from_response_and_form(response, form)
        response = self.session.post(form_action, data=form_data)
        soup = bs4.BeautifulSoup(response.text, 'html5lib')
        title = soup.find('title')
        form = soup.find(lambda tag: tag.name == 'form' and tag.get('name', '') == 'Login')
        inputs = form.find_all('input')
        form_data = {i['name']: i['value'] for i in inputs}
        form_data['IDToken0'] = ''
        form_data['IDToken1'] = em
        form_data['IDToken2'] = passwd
        form_data['IDButton'] = 'Sign In'
        form_action = self.form_action_from_response_and_form(response, form)
        response = self.session.post(form_action, data=form_data, allow_redirects=False)
        form_data = {inp['name']: inp['value'] for inp in inputs if inp['type'] != 'submit'}
        response = self._follow_redirects(response, redirect_uri)
        code = response.get('code', None)[0]
        state1 = response.get('state', None)[0]
        data = {
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
            'code': code,
            'client_id': user['client_id'],
            'client_secret': user['secret_key'],
            'self_contained_token': True
        }
        response = self.session.post("https://idbroker.webex.com/idb/oauth2/v1/access_token", data=data)
        oauth_token = response.json()
        print(oauth_token)
        return oauth_token

    def form_action_from_response_and_form(self,response, form):
        url = response.request.url
        parsed_url = urllib.parse.urlparse(url)
        result = urllib.parse.urljoin(url, form.get('action', parsed_url.path))
        return result

    def _follow_redirects(self,response, intercept_url='', response_type='code'):
        while response.status_code == 302:
            location = response.headers['location'].strip()
            loc_url = urllib.parse.urlparse(location)
            if response_type == 'code':
                if loc_url.query:
                    query = urllib.parse.parse_qs(loc_url.query)
                    if 'error' in query:
                        pass
                    if intercept_url and location.startswith(intercept_url):
                        return query
            location = urllib.parse.urljoin(response.request.url, location)
            response = self.session.get(location, allow_redirects=False)
        return response
