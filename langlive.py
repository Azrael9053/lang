import requests
import time
import os

def setting():
    ID = input("請輸入成員ID：")
    return ID

def filedownload(ID):
    mkdir('./' + ID +'ts_files/')
    with open(ID + 'ts.txt', 'r') as f:
        ts_list = f.readlines()
        # print(ts_list)

    for i in ts_list:
        url = 'https://video-ws-ak-hls.lv-play.com/live/' + ID + 'Y/' + i.replace('\n', '')
        r = requests.get(url)
        if r.status_code == 200:
            tspath = './' + ID +'ts_files/' + i.split('.')[0] +'.ts'
            print('正在下載' + i.split('.')[0] + '.ts')
            with open(tspath, "wb+") as file:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

        else:
            continue
        #     print("成員直播已結束即將下載一開始的直播")
        #     revdownload(n, id)
        #     break

        # time.sleep(2.5)
        # i += 1


def tsdownload(ID):
    m3u8_url = 'https://video-ws-ak-hls.lv-play.com/live/' + ID + 'Y/playlist.m3u8'
    ts_list = []
    flag = 0
    count = 0
    first_ts_flag = 0
    while True:
        r = requests.get(m3u8_url)
        if r.status_code == 200:
            ts_text = r.text
            for t in ts_text.split('\n'):
                if flag == 0 and 'TARGETDURATION' in t:
                    ts_time = t.split(':')[1]
                    flag = 1
                if '.ts' in t and t not in ts_list:
                    if first_ts_flag == 0:
                        first_ts = t
                        # print(first_ts)
                        first_ts_flag = 1
                    ts_list.append(t)
                    print(t + '已新增至記事本')
                    with open(ID + 'ts.txt', 'a') as f:
                        f.write(t)
                        f.write('\n')
            # print(ts_time)
            time.sleep(int(ts_time))

        else:
            if count % 5 == 0:
                print('尋找中')
            count += 1
            time.sleep(3)

        if count == 100:
            print('end')
            return 0

def revdownload(n, ID):
    x = 0
    while True:
        n -= 1
        url = 'https://video-ws-ak-hls.lv-play.com/live/' + ID + 'Y/' + str(n) + '.ts?wsApp=HLS&wsMonitor=0'
        r = requests.get(url)
        if r.status_code == 200:
            mkdir('./' + ID + 'ts_files/')
            tspath = './' + ID + 'ts_files/' + str(n) + '.ts'
            print('正在下載' + str(n) + '.ts')
            with open(tspath, "wb+") as file:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

        else:
            x += 1
        if x == 20:
            print("下載結束!")
            break


def marge(ID):
    file_list = []
    for root, dirs, files in os.walk('./' + ID +'ts_files/'): # 生成器
        dirs.sort()
        for fn in files:
            p = str(root+'/'+fn)
            file_list.append(p)
    # sorted(file_list)
    # print(file_list)
    # for p in file_list:
    #     print(p)
    mkdir('./合併檔案')
    file_path = './合併檔案/' + ID + '.ts'
    with open(file_path, 'wb+') as fw:
        for i in range(len(file_list)):
            fw.write(open(file_list[i], 'rb').read())

def mkdir(path):
    f = os.path.exists(path)
    if not f:
        os.makedirs(path)

ID = None
while True:
    try:
        sw = int(input("1：抓取ts檔  2：下載檔案  3：合併檔案  4：設定成員資料  5：下載開頭(test)  6：離開程式  7：一鍵下載\n"))

    except ValueError:
        print('請輸入數字！')
        continue
    if sw == 1:
        if ID == None:
            ID = setting()

        tsdownload(ID)

    elif sw == 2:
        if ID == None:
            ID = setting()

        p = os.path.exists('./' + str(ID) + 'ts.txt')
        if not p:
            print('找不到檔案')
        else:
            filedownload(ID)

    elif sw == 3:
        if ID == None:
            ID = setting()

        marge(ID)

    elif sw == 4:
        ID = setting()

    elif sw == 5:
        if ID == None:
            ID = setting()

        n = input("複製.txt的第一行文字貼在這邊(EX:1592925034.ts?wsApp=HLS&wsMonitor=0)：")
        revdownload(int(n.split('.')[0]), ID)

    elif sw == 6:
        print('byebye!')
        input('按任意鍵離開')
        break

    elif sw == 7:
        if ID == None:
            ID = setting()

        m3u8_url = 'https://video-ws-ak-hls.lv-play.com/live/' + ID + 'Y/playlist.m3u8'
        temp = 0
        while True:
            r = requests.get(m3u8_url)
            if r.status_code == 200:
                temp = 1
                tsdownload(ID)
                p = os.path.exists('./' + str(ID) + 'ts.txt')
                if not p:
                    print('找不到檔案')
                else:
                    filedownload(ID)
                    with open(str(ID) + 'ts.txt', 'r') as tstxt:
                        n = tstxt.readlines()[0].replace('\n', '')
                    revdownload(int(n.split('.')[0]), ID)
                    marge(ID)
                    print('檔案下載合併完成')
                    input('按任意鍵離開')

            elif temp == 1:
                break

            else:
                print('尋找中')
                time.sleep(30)

        if temp == 1:
            temp = 0
            break

    else:
        print('請輸入1~7')
