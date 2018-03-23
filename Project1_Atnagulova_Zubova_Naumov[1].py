import os
import re

def folders():
    """Функция нужна для создания словаря для определения вида спорта,
    использовались папки BB, Biatlon, FB, FS, Hockey, Tennis"""
    dic = {}
    for root, dirs, files in os.walk('Tennis'):
        for fname in files:
            arr = token_dic(root + '/' + fname)
            for one_a in arr:
                if one_a in dic:
                    dic[one_a] += 1
                else:
                    dic[one_a] = 1
    for word in sorted(dic, key=lambda w: dic[w], reverse=True)[:101]:
        print('{}\t{}'.format(dic[word], word))

def sport_dic():
    """Функция нужна для создания словаря для определения вида спорта"""
    dic_sports = {}
    for root, dirs, files in os.walk('Dics'):
        for fname in files:
            arr = []
            f = open(root + '/' + fname, 'r', encoding = 'utf-8')
            text = f.read()
            f.close()
            text = text.split('\n')
            for a in text:
                a = a.split(';')
                arr.append(a[1])
            dic_sports[fname[4:-4]] = arr
    return dic_sports

def token_dic(value):
    arr = []
    f = open(value, 'r', encoding = 'utf-8')
    text = f.read().lower()
    f.close()
    text = text.split('\n')
    for a in text:
        a = a.split(' ')
        for one_a in a:
            one_a = one_a.strip('.-,!? \'"')
            arr.append(one_a)
    return arr

def splitter(root, fname, ind):
    if not os.path.exists('Corp_splitted'):
        os.makedirs('Corp_splitted')
    arr = []
    path1 = 'Corp_splitted/'+'id'+str(ind)+'_'+fname[:-4]+'_splits'+fname[-4:]
    with open(root + '/' + fname, 'r', encoding = 'utf-8') as f:
        text = f.readlines()
    f.close()
    f1 = open(path1, 'w', encoding = 'utf-8')
    for a in text:
        a = re.sub('( ?[!.?]+?) ?([а-яёА-ЯЁ0-9]+?)', '\\1\n\\2', a)
        if re.search('\\w', a) is not None:
            arr.append(a)
            f1.write(a)
    f1.close()
    ind += 1
    return arr

def tokens(value):
    dic_sports = value
    ind = 1
    if not os.path.exists('Corp_tokenized'):
        os.makedirs('Corp_tokenized')
    for root, dirs, files in os.walk('Corp'):
        for fname in files:
            path1 = 'Corp_tokenized/'+'id'+str(ind)+'_'+ fname[:-4] + '_tokens' + fname[-4:]
            dic_dic = {}
            arr = token_dic(root + '/' + fname)
            for elem in arr:
                for sport in dic_sports:
                    if elem in dic_sports[sport]:
                        if sport in dic_dic:
                            dic_dic[sport] += 1
                        else:
                            dic_dic[sport] = 1
            file_sport = sorted(dic_dic, key=lambda w: dic_dic[w], reverse=True)[0]
            #print(file_sport)
            w_id = 1
            arr_sent = splitter(root, fname, ind)
            if file_sport == 'hockey':
                f = open(path1, 'w', encoding = 'utf-8')
                for a in hockey_tokens(arr_sent):
                    f.write(str(w_id) + '\t' + a + '\n')
                    w_id += 1
                f.close()
                ind += 1
            if file_sport == 'football':
                f = open(path1, 'w', encoding = 'utf-8')
                for a in fb_tokens(root + '/' + fname):
                    f.write(str(w_id) + '\t' + a + '\n')
                    w_id += 1
                f.close()
                ind += 1
            if file_sport == 'basketball':
                f = open(path1, 'w', encoding = 'utf-8')
                for a in bb_tokens(root + '/' + fname):
                    f.write(str(w_id) + '\t' + a + '\n')
                    w_id += 1
                f.close()
                ind += 1
            if file_sport == 'biatlon':
                f = open(path1, 'w', encoding = 'utf-8')
                for a in biatlon_tokens(root + '/' + fname):
                    f.write(str(w_id) + '\t' + a + '\n')
                    w_id += 1
                f.close()
                ind += 1
            if file_sport == 'tennis':
                f = open(path1, 'w', encoding = 'utf-8')
                for a in tennis_tokens(root + '/' + fname):
                    f.write(str(w_id) + '\t' + a + '\n')
                    w_id += 1
                f.close()
                ind += 1
                

def tennis_tokens(fname):
    arr = []
    f = open(fname, 'r', encoding = 'utf-8')
    text = f.read()
    f.close()
    text = re.sub('([0-9]+?:[0-9]+?). ([\\w]+?)', '\\1\n\\2', text)
    text = text.split('\n')
    for word in text:
        word = word.split()
        for one in word:
            one = one.strip('.,!?)')
            if re.search('\\w', one) is not None:
                if re.search('[\\w]+?/[\\w]+?', one) is not None:
                    one = one.split('/')
                    for elem in one:
                        arr.append(elem)
                else:
                    if ('(' or '[' or '{') in one:
                            one = re.sub('[({\[]([\\w]+?)', '\\1', one)
                    arr.append(one)
    return arr

def hockey_tokens(arr_sent):
    arr = []
    for sent in arr_sent:
        timing = re.findall('([0-9]{2}:[0-9]{2})', sent)
        for tim in timing:
            arr.append(tim)
        if ' ' in sent:
            for segm in sent.split():
                segm = segm.strip('.?:;,)]}!')
                if re.search('\\w.*?', segm) is not None:
                    if ('(' or '[' or '{') in segm:
                        segm = re.sub('[({\[]([\\w]+?)', '\\1', segm)
                    if '»' in segm and '«' not in segm:
                        segm = re.sub('([\\w]+?)»', '\\1', segm)
                    if '«' in segm and '»' not in segm:
                        segm = re.sub('«([\\w]+?)', '\\1', segm)
                    long = re.search('(-[А-ЯЁ]-)+', segm)
                    if long is not None:
                        segm = re.sub('(-[А-ЯЁ])(-[А-ЯЁ])(-[А-ЯЁ])', '\\1\\3', segm)
                    arr.append(segm)
    return arr

def bb_tokens(fname):
    arr = []
    f = open(fname, 'r', encoding = 'utf-8')
    text = f.read()
    f.close()
    text = text.split('\n')
    for word in text:
        word = word.split()
        for one in word:
            one = one.strip('.,!?)')
            if re.search('\\w', one) is not None:
                if ('(' or '[' or '{') in one:
                    one = re.sub('[({\[]([\\w]+?)', '\\1', one)
                arr.append(one)
    return arr

def fb_tokens(fname):
    splits = []
    text_file = open(fname,  'r', encoding = 'UTF-8').read().replace('.', '').replace(',', '').split()
    for i in text_file:
        splits.append(i)
    return splits

def biatlon_tokens(fname):
    splits = []
    text_file = open(fname,  'r', encoding = 'UTF-8').read().replace('.', '').replace(',', '').split()
    for i in text_file:
        splits.append(i)
    return splits



#sport_dic()
tokens(sport_dic())
