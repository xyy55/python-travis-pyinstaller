import os
import pandas as pd
import re

input_path = os.getcwd() + '\\输入文件夹\\'
output_path = os.getcwd() + '\\输出文件夹\\'
pattern = re.compile(r"冠字号\*+(.+?)\*+冠字号结束") #筛选冠字号的正则表达式
time_pattern = re.compile(r"(\d{2}\:\d{2}:\d{2}) +?(送钞成功|钞币存入)") #筛选时间的正则表达式
date_pattern = re.compile(r"日期:(\d{4}-\d{2}-\d{2})") #筛选日期的正则表达式

print("""
请选择工作模式：
1、提取两个文件的冠字号并作对比
2、批量提取文件夹内文件冠字号
输入数字后回车
      """)
      
num = input().strip()
files = os.listdir(input_path)

def read_txt(path):
  f = open(path,encoding='utf-8')
  txt = ''
  for line in f :
    txt = txt + line
  f.close()
  return txt

def get_gzh(txt):
  data = txt.split('\n\n')
  gzhs = []
  times = []
  opts = []
  for d in data:
    d = d.replace('\n',' ')
    result = re.findall(pattern, d)
    if len(result) == 0:
      continue
    time = re.findall(time_pattern, d)[0][0]
    opt = re.findall(time_pattern, d)[0][1]
    date = re.findall(date_pattern, d)[0]
    for i in result:
      for gzh in i.split(" "):
        if gzh != '':
          gzhs.append(gzh)
          times.append(date+' '+time)
          if opt == '送钞成功':
            opts.append('取钱')
          elif opt == '钞币存入':
            opts.append('存钱')
    
  return gzhs, times, opts

def get_col_name(path):
  _, full_name = os.path.split(path)
  col_name, _ = os.path.splitext(full_name)
  return col_name

if num == '1':
  if len(files) != 2:
    input("输入文件夹内有且只能有两个文件，请确认。。。")
  else:
    dfs = []
    col_names = []
    for file in files:
      col_name = file.strip('.txt')
      col_names.append(col_name)
      txt = read_txt(input_path+file)
      gzh,time,opt = get_gzh(txt)
      dfs.append(pd.DataFrame({col_name:gzh, '交易时间':time,'操作类型':opt}).sort_values(by='交易时间').reset_index(drop=True))
    df = pd.merge(dfs[0], dfs[1],left_on=files[0].strip('.txt'),right_on=files[1].strip('.txt'),how='inner')
    df.to_excel(output_path + '对比结果.xlsx',index=False)
    input('处理成功，按任意键结束。。。')
elif num == '2':
  dfs = []
  col_names = []
  for file in files:
    col_name = file.strip('.txt')
    col_names.append(col_name)
    txt = read_txt(input_path+file)
    gzh,time,opt = get_gzh(txt)
    dfs.append(pd.DataFrame({col_name:gzh, '交易时间':time,'操作类型':opt}).sort_values(by='交易时间').reset_index(drop=True))
  df = pd.concat(dfs,axis=1, join='outer')
  df.to_excel(output_path + '批量处理结果.xlsx',index=False)
  input('处理成功，按任意键结束。。。')

else:
  input('不要乱输入，按任意键结束。。。')
