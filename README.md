# cloudflare-subdomain-dydns
dynamic dns for sub domains on cloudflare


This project is hopefully filling the hole of there being no simple options for modifiying subdomains on cloudflare


For the config file you need to get your cloudflare api key which can be found or generated on My profile, api keys, global api key, api key for your api key. Cloudflare support question with further explanation: https://support.cloudflare.com/hc/en-us/articles/200167836-Where-do-I-find-my-Cloudflare-API-key- 

Modify the config, the brackets (<,>) are what to change

Set whether you need ssh or not at the subdomain, if  you do need ssh, then make sure that you set ssh to "True" that will set cloudflare proxy to off 
setting cron for the script:

run: `~/ contab -e`

Append the following and save it should let you know the cron has been saved

*/5 * * * * /usr/bin/python3 /home/<user>\<git location\>/dydns.py

