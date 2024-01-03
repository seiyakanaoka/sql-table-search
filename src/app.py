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

# データ型を取得する
def find_data_type(value, data_type_list):
  for data_type in data_type_list:
      is_type = data_type in value
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
        column_list_without_newlines = column_content.replace("\n", " ")
        column_list_with_single_space = re.sub(r'\s+', ' ', column_list_without_newlines)
        start_index = column_list_with_single_space.find("(")

        new_column_content_list = column_list_with_single_space[start_index + 1:]
        column_list = new_column_content_list.split(",")

        new_column_list = list(filter(lambda column: "CONSTRAINT" not in column, column_list))
        name_list = [item.split()[0] for item in new_column_list]
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