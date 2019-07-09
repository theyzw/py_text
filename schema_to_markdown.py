import re


def delete_symbol(str):
    """删除符号
    """
    str = str.strip().strip('\'').strip('`')
    return str


def first_symbol_after_index(text, index, symbol):
    """index位置之后第一个symbol
    """
    last_index = text.find(symbol, index)
    return last_index


result = ''
# 读取文件
with open('region.sql', 'r') as fo:
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
    # 从start开始找往后第一个;
    last_index = first_symbol_after_index(text, m.start(), ';')
    ddl.append(text[m.start():last_index])

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
    first_bracket_index = first_symbol_after_index(sql, 0, '(')
    table_name = sql[len(sub_create_table): first_bracket_index]
    table_name = delete_symbol(table_name)
    header += '(' + table_name + ')'
    result += header

    result += '\n\n' + '|字段名称|类型|非空|默认值|说明|' + '\n' \
        + '|:--|:--|:--|:--|:--|' + '\n'

    # 最后一个)
    last_bracket_index = sql.rfind(')')
    row_sql = sql[first_bracket_index + 1: last_bracket_index]

    print(row_sql)

    # 主键位置
    for pk in re.finditer(row_sql, 'primary key'):
        print(222)
        # pk位置之后第一个,
        index = first_symbol_after_index(row_sql, pk.start(), ',')
        pk_str = row_sql[pk.start(): index]
        print(11111)
        print(pk_str)

    # 索引

    # print(row_sql)

    # lines = row_sql.split(',\n')

    # for line in lines:
    # print(line)

    # 索引

    result += '\n\n'

print(result)
