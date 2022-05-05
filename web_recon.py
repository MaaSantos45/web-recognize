import sys
import threading

import requests
import dns.resolver

RESOLVER = dns.resolver.Resolver()
WORDLIST = []
THREADS = []
USAGE = (""" usage: python3 web_recon.py <domain> <wordlist file.txt> <option>

            Options
                -s <protocol> Subdomain Bruteforce
                -S <protocol> <specify directory> (to append a specific directory)
                -d <protocol> Directory Bruteforce (subdomain www)
                -D <protocol> <specify subdomain> (to append a specific subdomain)
    """)

def brute_directory(domain, sub="", protocol="http"):
    word = WORDLIST.pop(0)
    try:
        url = "{}://{}.{}".format(protocol,sub, domain)
        if sub == "":
            url = "{}://www.{}".format(protocol, domain)
        url_final = "{}/{}".format(url, word)
        response = requests.get(url_final)
        code = response.status_code
        if code != 404:    
            print ("{} : {}".format(url_final,code))
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as error:
        print (error)
        sys.exit(0)
            


def brute_subdomain(domain, dict=""):
    try:
        subdomain = WORDLIST.pop(0)
        try:
            target = "{}/{}".format(domain, dict)
            if dict == "":
                target = domain
            sub_target = "{}.{}".format(subdomain, target)
            try:
                results = RESOLVER.resolve(sub_target, "A")
                for result in results:
                    print("{} => {}".format (sub_target,result))
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass
        except KeyboardInterrupt:
            sys.exit(0)
    except Exception as error:
        print (error)
        sys.exit(0)
            


if __name__== "__main__":
    try:
        args = sys.argv
        if len(args) >= 3:
            domain = sys.argv[1]
            wordlist_path = sys.argv[2]
            option = ()
            protocol = "http"
            if len(args) >= 4:
                option = sys.argv[3]
                protocol = "http"
                if len (args) >=5:
                    protocol = sys.argv[4]
                    if len(args) >= 6:
                        specify = sys.argv[5]
        else:
            print(USAGE)
            sys.exit()
    except Exception as error:
        print(error)
        sys.exit()
    try:
        with open (wordlist_path, "r") as file:
            WORDLIST = file.read().splitlines()
            if option:                
                if option == "-s":
                    while True:
                        try:
                            t = threading.Thread(target=brute_subdomain(domain=domain))
                            THREADS.append(t)
                        except:
                            break
                elif option == "-S":
                    while True:
                        try:
                            t = threading.Thread(target=brute_subdomain(domain=domain, dict=specify))
                            THREADS.append(t)
                        except:
                            if not specify:
                                print (USAGE)
                            break
                elif option == "-d":
                    while True:
                        try:
                            t = threading.Thread(target=brute_directory(domain=domain, protocol=protocol))
                            THREADS.append(t)
                        except:
                            break
                elif option == "-D":
                    while True:
                        try:
                            t = threading.Thread(target=brute_directory(domain=domain, sub=specify, protocol=protocol))
                            THREADS.append(t)
                        except:
                            if not specify:
                                print (USAGE)
                            break
                else:
                    sys.exit()
            else:
                print(USAGE)
    except Exception as error:
        print (USAGE)
        print(error)
    

    for t in THREADS:
        t.start()

    for t in THREADS:
        t.join()