// カラムの整形
function formatColumns(columnValues) {
  var columnList = columnValues.filter((column) => column !== '')
  return columnList.map((value, i) => {
    if (i === 0) {
      return `${value}`;
    }
    return ` ${value}`
  }).join(',')
}

function isString(value) {
  var srtringTypeList = [
    'CHAR',
    'VARCHAR',
    'TINYTEXT',
    'TEXT',
    'MEDIUMTEXT',
    'LONGTEXT',
    'ENUM',
    'SET',
    'DATE',
    'TIME',
    'DATETIME',
    'TIMESTAMP',
    'YEAR'
  ];
  for (let i = 0; i < srtringTypeList.length; i++) {
        if (value.includes(srtringTypeList[i])) {
            return true;
        }
    }
  return false;
}

function isInt(value) {
  var intTypeList = [
    'TINYINT',
    'SMALLINT',
    'MEDIUMINT',
    'INT',
    'BIGINT',
    'FLOAT',
    'DOUBLE',
    'DECIMAL'
  ];
  for (let i = 0; i < intTypeList.length; i++) {
        if (value.includes(intTypeList[i])) {
            return true;
        }
    }
  return false;
}

function isBoolean(value) {
  if(value.includes('BOOLEAN')) {
    return true;
  }
  return false;
}

// 型チェック
function typeCheck(value, type) {
  if(value.toString().toUpperCase() === 'NULL') {
    return 'NULL';
  }
  if(isString(type)) {
    // ハイフンの場合は、シングルクォートのみの空文字を返す
    if(value === '-') {
      return `''`;
    }
    return `'${value}'`;
  }
  if (isBoolean(type)) {
    if (value.toString().toLowerCase() === 'true') {
      return true.toString().toUpperCase();
    }
    return false.toString().toUpperCase();
  }
  return value;
}

// データの取得
function getInsertValues(dataValues, types) {
  var result = dataValues.map((dataValue, firstIndex) => {
    var dataList = dataValue.filter((data) => data !== '')
    var formatValues = dataList.map((data, secondIndex) => {
      var type = types[secondIndex]
      if (secondIndex === 0) {
        return typeCheck(data, type);
      }
      // 2つ目以降の値は、値の前に空白をつける
      return ` ${typeCheck(data, type)}`
    });

    // 文字列に変換
    var result = formatValues.join(',');

    if (firstIndex === 0) {
      return `(${result})`
    }
    // 2つ目以降の値は、値の前に空白をつける
    return ` (${result})`
  });

  // 文字列に変換して返す
  return result.join(',');
}

function myFunction() {
  var spreadSheet = SpreadsheetApp.getActiveSpreadsheet();
  var activeSheet = spreadSheet.getActiveSheet()

  // テーブル名の取得
  var tableName = activeSheet.getRange('C13').getValue();

  // データが入っている最終列を取得
  var lastColumn = activeSheet.getLastColumn();

  // カラムの値を取得
  var columnValues = activeSheet.getRange(15, 3, 1, lastColumn).getValues()[0];
  
  var columns = formatColumns(columnValues);

  // 型定義を取得
  var typeValues = activeSheet.getRange(16, 3, 1, lastColumn).getValues()[0];

  var types =  typeValues.filter((value) => {
    return value !== '';
  });

  // データが入っている最終行を取得
  var lastRow = activeSheet.getLastRow()
  var dataValues = activeSheet.getRange(17, 3, lastRow - 16, lastColumn).getValues();

  // データの取得
  var insertValues = getInsertValues(dataValues, types);
  
  var format = [[`INSERT INTO ${tableName} (${columns}) VALUES ${insertValues};`]]

  activeSheet.getRange('E4').setValues(format);
}
