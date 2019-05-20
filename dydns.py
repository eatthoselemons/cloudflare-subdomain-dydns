import requests
import pprint 
import configparser

def get_ip_addr():
    r = requests.get('http://ip4only.me/api')
    return_string = str (r.content).split(',')
    return return_string[1]

config = configparser.ConfigParser()
config.read('dydns.config')
#Cloudflare Username
cloudflare_username = config['credentials']['cloudflare username']
#Api key from cloudflare for your account
cloudflare_api_key = config['credentials']['cloudflare api key']
#The domain name to change
domain_name = config['domain information']['domain name']
#the subdomain to change
sub_domain = config['domain infomation']['sub domain']
#whether or not you need ssh, if you want ssh you cannot use cloudflare proxie
ssh = config['domain infomation']['use ssh']

#urls for cloudflares v4 api
user_url = "https://api.cloudflare.com/client/v4/user"
zone_url = "https://api.cloudflare.com/client/v4/zones"

#get the current ip address uses 'http://ip4only.me/api' which returns a csv with the external ip address
ip_addr = get_ip_addr()

#authentication headers
headers = {"X-Auth-Email": cloudflare_username, "X-Auth-Key": cloudflare_api_key, "Content-Type": "application/json"}

# json for the regular sub domain
#   we flip ssh because if we want ssh, we cannot have it proxied ie ssh=True,proxied=False; ssh=False,proxied=True
json = {"type" : "A", "name": sub_domain + '.' + domain_name,"content":ip_addr,"proxied": not ssh}

#grab the zone id, which is basically the identifier for the domain
zone_url_get = zone_url + "?name=" + domain_name
r = requests.get(zone_url_get,headers=headers)
zone_id = r.json()['result'][0]['id']

#grab the sub domains under a zone (domain) 
url = zone_url + '/' + zone_id + '/dns_records?type=A'
r = requests.get(url,headers=headers)

#check if the domain exists if so break; if not create it
for item in r.json()['result']:
    if item['name'] == sub_domain + '.' + domain_name:
        break
    else:
        url = zone_url + '/' + zone_id + '/dns_records'
        r = requests.post(url,json=json,headers=headers)
        if r.json()['success'] == True:
            print('made the sub domain')
        else:
            pp = pprint.PrettyPrinter(indent=2)
            pp.pprint(r.json())
            print("--------------------------------------------------")
            raise Exception('could not create the sub domain, check your information')
            
#get the new sub domain id
url = zone_url + '/' + zone_id + '/dns_records?type=A&name=' + sub_domain +'.'+ domain_name
r = requests.get(url, headers=headers)
sub_domain_id = r.json()['result'][0]['id']

#update the sub domain address
url = zone_url + '/' + zone_id + '/dns_records/' + sub_domain_id 
r = requests.put(url,headers=headers,json=json)

#verify that the ip addresses are the same 
url = zone_url + '/' + zone_id + '/dns_records?type=A&name=' + sub_domain + '.' + domain_name
r = requests.get(url, headers=headers)
print("checking if the sub domain is correct")
print("ip4.me address: {}".format(ip_addr))
print("cloudflare ip address: {}".format(r.json()['result'][0]['content']))
