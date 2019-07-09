

result = ''
with open('delete.log', 'r') as fo:
    while True:
        line = fo.readline()
        # 读取完毕
        if not line:
            break
        # 去掉首尾空格
        line = line.strip()
        # 空行
        if not line:
            continue
        index = line.find('profile_id')
        profile_id = line[index + 11:]
        result += profile_id + ','

if result:
    result = result[:-1]
print(result)
