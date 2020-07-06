import requests
import time
import os
import threading

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}


def todownload(t):
    mkdir('./' + Year + '_' + month + '_' + day + ' ' + ID + 'ts_files/')
    url = 'https://video-ws-ak-hls.lv-play.com/live/' + ID + 'Y/' + t
    r = requests.get(url, headers = headers)
    if r.status_code == 200:
        tspath = './' + Year + '_' + month + '_' + day + ' ' + ID + 'ts_files/' + t.split('.')[0] + '.ts'
        print('正在下載' + t.split('.')[0] + '.ts')
        with open(tspath, "wb+") as file:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

    else:
        with open(Year + '_' + month + '_' + day + ' ' + ID + 'failQQ.txt', 'a') as f:
            f.write('https://video-ws-ak-hls.lv-play.com/live/' + ID + 'Y/' + t)
            f.write('\n')
        print(t + '下載失敗')



def setting():
    ID = input("請輸入成員ID：")
    # ID = '3619520'
    return ID

def failfiledownload(ID):
    mkdir('./' + Year + '_' + month + '_' + day + ' ' + ID + 'ts_files/')
    with open(Year + '_' + month + '_' + day + ' ' + ID + 'failQQ.txt', 'r') as f:
        ts_list = f.readlines()
        # print(ts_list)

    for i in ts_list:
        url = i.replace('\n', '')
        dlcount = 0
        while dlcount < 20:
            r = requests.get(url, headers = headers)
            if r.status_code == 200:
                dlcount = 0
                tspath = './' + ID +'ts_files/' + i.split('.')[2].replace('com/live/' + ID + 'Y/', '') +'.ts'
                print('正在下載' + i.split('.')[2].replace('com/live/' + ID + 'Y/', '') + '.ts')
                with open(tspath, "wb+") as file:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)

            else:
                dlcount += 1


def tsdownload(ID):
    m3u8_url = 'https://video-ws-ak-hls.lv-play.com/live/' + ID + 'Y/playlist.m3u8'
    ts_list = []
    flag = 0
    count = 0
    tflag = 0
    first_ts_flag = 0
    while True:
        r = requests.get(m3u8_url, headers = headers)
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
                    if tflag == 1:
                        thh.join()
                    thh = threading.Thread(target=todownload(t))
                    thh.start()
                    tflag = 1
                    print(t + '已新增至記事本')
                    with open(Year + '_' + month + '_' + day + ' ' + ID + '_' + 'ts.txt', 'a') as f:
                        f.write('https://video-ws-ak-hls.lv-play.com/live/' + ID + 'Y/' + t)
                        f.write('\n')
            # print(ts_time)
            time.sleep(1)
            count = 0

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
        r = requests.get(url, headers = headers)
        if r.status_code == 200:
            mkdir('./' + Year + '_' + month + '_' + day + ' ' + ID + 'ts_files/')
            tspath = './' + Year + '_' + month + '_' + day + ' ' + ID + 'ts_files/' + str(n) + '.ts'
            # print(str(n) + '.ts?wsApp=HLS&wsMonitor=0' + '已新增至記事本')
            # with open(Year + '_' + month + '_' + day + ' ' + ID + 'failQQ.txt', 'a') as f:
            #     f.write('https://video-ws-ak-hls.lv-play.com/live/' + ID + 'Y/' + str(n) + '.ts?wsApp=HLS&wsMonitor=0')
            #     f.write('\n')
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
    for root, dirs, files in os.walk('./' + Year + '_' + month + '_' + day + ' ' + ID + 'ts_files/'): # 生成器
        # dirs.sort()
        for fn in files:
            p = str(root+'/'+fn)
            file_list.append(p)

    newlist = sorted(file_list)
    # for p in file_list:
        # print(p)
    mkdir('./合併檔案')
    file_path = './合併檔案/' + Year + '_' + month + '_' + day + ' ' + ID + '.ts'
    with open(file_path, 'wb+') as fw:
        for i in range(len(newlist)):
            fw.write(open(newlist[i], 'rb').read())

def mkdir(path):
    f = os.path.exists(path)
    if not f:
        os.makedirs(path)




ID = setting()

try:
    print('設定程式啟動日期')
    print('當天可以直接按Enter')
    print('範例(12/23)')
    try:
        startday = input('請輸入日期:')
        timetuple = time.localtime()
        tlist = list(timetuple)
        # print(tlist)
        tlist[1] = int(startday.split('/')[0])
        tlist[2] = int(startday.split('/')[1])

    except:
        pass
    print('設定程式啟動時間，請輸入24小時制')
    print('直接開始請按Enter')
    print('範例(18:00) !!!!!冒號請用半形!!!!!')
    starttime = input('請輸入時間:')
    timelist = starttime.split(':')
    tlist[3] = int(timelist[0])
    tlist[4] = int(timelist[1])
    tlist[5] = 0
    timetuple = tuple(tlist)
    timecount = 0
    while True:
        if time.mktime(timetuple) < time.mktime(time.localtime()):
            print('程式開始執行!')
            break
        else:
            # print('現在時間:', time.strftime("%b %d %Y %H:%M:%S", time.localtime()), end = '')
            # for i in range(29):
            time.sleep(1)
            # timecount += 1
            # if timecount % 60 == 0:
            os.system('cls')
            print('下載成員ID :', ID)
            print('現在時間 :', time.strftime("%b %d %Y %H:%M:%S", time.localtime()))
            print('設定下載開始時間 :', time.strftime("%b %d %Y %H:%M:%S", timetuple))
            # print('\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b')


except:
    # print('test')
    print('程式開始執行!')


m3u8_url = 'https://video-ws-ak-hls.lv-play.com/live/' + ID + 'Y/playlist.m3u8'
temp = 0
Year = time.strftime('%Y',time.localtime())
month = time.strftime('%m',time.localtime())
day = time.strftime('%d',time.localtime())




while True:
    r = requests.get(m3u8_url, headers = headers)
    if r.status_code == 200:
        temp = 1
        tsdownload(ID)
        p = os.path.exists(Year + '_' + month + '_' + day + ' ' + str(ID) + '_' + 'ts.txt')
        if not p:
            print('找不到檔案')
        else:
            # filedownload(ID)
            with open(Year + '_' + month + '_' + day + ' ' + str(ID) + '_' + 'ts.txt', 'r') as tstxt:
                n = tstxt.readlines()[0].replace('\n', '')
            revdownload(int(n.split('.')[2].replace('com/live/' + ID + 'Y/', '')), ID)
            if os.path.isfile('./' + ID + 'failQQ.txt'):
                ask = input('是否要重新下載失敗的檔案? y/n : ')
                if ask == 'y':
                    failfiledownload(ID)
            marge(ID)
            print('檔案下載合併完成')
            input('按ENTER鍵離開')

    elif temp == 1:
        break

    else:
        print('尋找中')
        time.sleep(30)
