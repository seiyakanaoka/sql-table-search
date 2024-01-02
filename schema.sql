CREATE TABLE user_id (
    id VARCHAR(255) NOT NULL COMMENT 'ユーザーID'
    , sub_number INT NOT NULL COMMENT '枝番'
    , create_datetime DATETIME NOT NULL COMMENT '作成日時'
    , update_datetime DATETIME COMMENT '更新日時'
    , CONSTRAINT user_id_PKC PRIMARY KEY (id)
) COMMENT 'ユーザーID' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC;

CREATE TABLE user (
    id VARCHAR(255) NOT NULL COMMENT 'ユーザーID'
    , name VARCHAR(255) NOT NULL COMMENT 'ユーザー名'
    , file_id VARCHAR(36) NOT NULL COMMENT 'ファイルID'
    , image_id VARCHAR(36) COMMENT '画像ID'
    , create_datetime DATETIME NOT NULL COMMENT '作成日時'
    , update_datetime DATETIME COMMENT '更新日時'
    , CONSTRAINT user_id_PKC PRIMARY KEY (id)
) COMMENT 'ユーザー' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC;
