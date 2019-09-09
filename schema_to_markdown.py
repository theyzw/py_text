import sys
import re


def delete_symbol(str):
    """删除左右符号
    """
    str = str.strip().strip('\'').strip('`')
    return str


def delete_blank(str):
    """删除空格
    """
    str = str.replace(' ', '')
    return str


def first_symbol_after_index(text, index, symbol):
    """index位置之后第一个symbol
    """
    last_index = text.find(symbol, index)
    return last_index


file_name = sys.argv[1]
# file_name = 'test.sql'

result = ''
# 读取文件
with open(file_name, 'r') as fo:
    text = fo.read()
    # 全部字符转小写
    text = text.lower()

'''
create table到下一个;之间是一整条建表语句
'''
sub_create_table = 'create table'
ddl = []
# 查找create table出现的所有位置
for m in re.finditer(sub_create_table, text):
    if not m:
        break
    # 从start开始找往后第一个;+换行
    last_index = first_symbol_after_index(text, m.start(), ';\n')
    ddl.append(text[m.start():last_index])

key_col_name = 'name'
key_col_type = 'type'
key_col_allow_null = 'allow_null'
key_col_default = 'default'
key_col_comment = 'comment'

sub_table_comment = 'comment='
for sql in ddl:
    # 主键
    primary_key = ''
    # 索引
    key = []
    header = '### '
    # 查找表注释
    table_comment_index = sql.find(sub_table_comment)
    if table_comment_index != -1:
        table_comment = sql[table_comment_index + len(sub_table_comment):]
        table_comment = delete_symbol(table_comment)
        header += table_comment
    # 查找表名
    # create table之后第一个(
    create_left_bracket_index = first_symbol_after_index(sql, 0, '(')
    table_name = sql[len(sub_create_table): create_left_bracket_index]
    table_name = delete_symbol(table_name)
    header += '(' + table_name + ')'
    result += header

    result += '\n\n' + '|字段名称|类型|非空|默认值|说明|' + '\n' \
        + '|:----|:----|:----|:----|:----|' + '\n'

    # 最后一个)
    last_bracket_index = sql.rfind(')')
    row_sql = sql[create_left_bracket_index + 1: last_bracket_index]

    # 主键或者key最先出现的位置
    first_key_index = 0

    # 主键
    primary_key_text = 'primary key '
    pk_index = row_sql.find(primary_key_text)
    first_key_index = pk_index
    # pk位置之后第一个(
    pk_left_bracket_index = first_symbol_after_index(row_sql, pk_index, '(')
    # pk位置之后第一个)
    pk_right_bracket_index = first_symbol_after_index(row_sql, pk_index, ')')
    # primary key (`id`, `name`)
    pk_str = row_sql[pk_left_bracket_index + 1: pk_right_bracket_index]

    # 索引
    key_dict = {}
    sub_key = 'key `'
    # 查找key `出现的所有位置
    for k in re.finditer(sub_key, row_sql):
        if not k:
            break
        first_key_index = first_key_index if first_key_index < k.start()\
            else k.start()
        # start往后第一个`
        key_grave_index = first_symbol_after_index(
            row_sql, k.start() + len(sub_key), '`')
        key_name = row_sql[k.start() + len(sub_key): key_grave_index]
        # start往后第一个(
        key_left_bracket_index = first_symbol_after_index(
            row_sql, k.start() + len(sub_key), '(')
        # start往后第一个)
        key_right_bracket_index = first_symbol_after_index(
            row_sql, k.start() + len(sub_key), ')')
        key_value = row_sql[key_left_bracket_index +
                            1: key_right_bracket_index]
        key_dict[key_name] = key_value

    col_sql = row_sql[:first_key_index]

    # 按\n分割
    lines = col_sql.split('\n')
    for line in lines:
        if delete_blank(line) == '':
            continue
        col_dict = {}
        # 查询第一个`+空格
        col_grave_index = first_symbol_after_index(line, 0, '` ')
        name = line[: col_grave_index]
        name = delete_symbol(name)
        col_dict[key_col_name] = name
        # 类型
        # line中删除name
        line = line[col_grave_index + 2:]
        col_blank_index = first_symbol_after_index(line, 0, ' ')
        col_type = line[: col_blank_index]
        col_dict[key_col_type] = col_type
        # 是否null
        line = line[col_blank_index + 1:]
        allow_null = '是'
        if not line.startswith('not null'):
            allow_null = '否'
        col_dict[key_col_allow_null] = allow_null
        # defalut 找不到设置为undefined
        default_val = ''
        sub_default = 'default '
        default_index = line.find(sub_default)
        comment_index = line.find('comment')
        if default_index >= 0:
            default_text = line[default_index:comment_index]
            default_val = default_text.replace(sub_default, '')
            # current_timestamp
            if default_val.find('current_timestamp') >= 0:
                default_val = 'current_timestamp'
        col_dict[key_col_default] = default_val
        # comment
        comment = ''
        if comment_index >= 0:
            comment = line[comment_index + len('comment'):]
            comment = delete_symbol(comment)
            comment = comment.replace('\',', '')
        col_dict[key_col_comment] = comment

        for value in col_dict.values():
            result += '|' + value
        result += '|\n'

    # 索引表
    if len(pk_str) <= 0 and len(key_dict) <= 0:
        break

    result += '\n\n索引\n\n|名称|字段|\n|:----|:----|\n'

    if len(pk_str) > 0:
        result += '|主键|' + pk_str.replace('`', '') + '|\n'

    if len(key_dict):
        for key, value in key_dict.items():
            result += '|' + key + '|' + value.replace('`', '') + '|\n'

    result += '\n\n'

print(result)

# 写入文件
fw = open(file_name + '.md', 'w')
fw.write(result)
fw.close()
