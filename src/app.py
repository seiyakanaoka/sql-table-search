import re

DATA_TYPE_LIST = [
    "VARCHAR",
    "CHAR",
    "TINYTEXT",
    "MEDIUMTEXT",
    "LONGTEXT",
    "TEXT",
    "ENUM",
    "SET",
    "DATETIME",
    "TIMESTAMP",
    "DATE",
    "TIME",
    "YEAR",
    "TINYINT",
    "SMALLINT",
    "MEDIUMINT",
    "BIGINT",
    "INT",
    "FLOAT",
    "DOUBLE",
    "DECIMAL",
    "BOOLEAN"
]

# カラム列のみを抽出する
def selected_columns(table_line_list):
  column_line_list = list(filter(lambda table_line: not("CREATE TABLE" in table_line or "CONSTRAINT" in table_line), table_line_list))[:-1]
  return list(column_line_list)

# 各カラム列の不要な要素を削除する
def filtered_column_line_list(column_line_list):
  split_space_column_line_list = list(map(lambda column: column.split(" "), column_line_list))
  new_column_list = map(lambda columns: list(filter(lambda x: x not in ["", ","], columns)), split_space_column_line_list)
  return list(new_column_list)

# データ型を取得する
def find_data_type(value, data_type_list):
  for data_type in data_type_list:
      is_type = any(data_type in s for s in value)
      if is_type:
        return data_type
  return None

# テーブル定義を検索し、カラム名とその型定義を取得する
def search_table(table_name, file_path):
  try:
    # SQLファイルを読み込む
    with open(file_path, 'r') as file:
        sql_content = file.read()
        pattern = re.compile(fr'CREATE TABLE {table_name} .*? \((.*?)\) COMMENT', re.DOTALL)
        table_match = pattern.search(sql_content)
        if not table_match:
          return

        column_content = table_match.group(0)
        columns_split_newline = list(map(lambda column: column, column_content.split("\n")))

        column_line_list = selected_columns(columns_split_newline)
        new_column_list = filtered_column_line_list(column_line_list)
        name_list = [item[0] for item in new_column_list]
        type_list = [find_data_type(item, DATA_TYPE_LIST) for item in new_column_list]
        result = { "name_list": name_list, "type_list": type_list }
        return result
  except FileNotFoundError:
        print(f'Error: File "{file_path}" not found.')
        return

# ユーザーからテーブル名を入力
table_name = input('テーブル名を入力してください: ')

# テーブルの存在を確認して結果を出力
columns = search_table(table_name, "schema.sql")

name_list = ",".join(columns["name_list"])

type_list = ",".join(columns["type_list"])

print(f"{table_name}テーブルカラム")
print("【カラム】")
print(f"> {name_list}")
print(" ")
print("【型定義】")
print(f"> {type_list}")
print(" ")