#清空path路径中（及子文件夹）codeblocks生成的多余文件及文件夹
#path 路径表示 样例 c:\\123\\33
#先判断是否是有效文件
#然后删除无效文件夹
#递归有效文件夹

import os
import shutil
def deluseless(path):
    allfile = os.listdir(path)
    for itr in allfile:        
        newpath = path + '\\\\' + itr;
        if os.path.isfile(newpath):
            fen = itr.split('.')
            houzhui = fen[-1]
            if houzhui == 'cbp' or houzhui == 'layout' or houzhui == 'depend':
                os.remove(newpath)
        if os.path.isdir(newpath):
            if itr == 'bin' or itr == 'obj':
                shutil.rmtree(newpath)
            else:
                deluseless(newpath)
        
path = 'C:\\Users\\Reynold\\Desktop\\2017 ccpc 网络赛08.19'
deluseless(path)