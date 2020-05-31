[toc]
# 量化金融

## 简述

数字理财

### 策略

1. boll
2. CCI
3. 恒定持仓份额做T

> 在横盘时,低吸。满足单位净值大于平均持仓成本是可卖出



## 工具

1. Python
2. vscode
3. MySQL

## 实现

### 建表

#### 基金信息表

```sql
CREATE TABLE `jj_dd_info` (
`id` VARCHAR ( 36 ) NOT NULL COMMENT '主键',
`jj_code` VARCHAR ( 36 ) DEFAULT NULL COMMENT '代码',
`jj_name` VARCHAR ( 36 ) DEFAULT NULL COMMENT '名称',
`jj_type` VARCHAR ( 36 ) DEFAULT NULL COMMENT '类型',
`comments` VARCHAR ( 5000 ) DEFAULT NULL COMMENT '备注',
PRIMARY KEY ( `id` ) USING BTREE 
) ENGINE = INNODB DEFAULT CHARSET = utf8;
```



#### 基础表

```sql

CREATE TABLE `jj_history` (
`id` VARCHAR ( 36 ) NOT NULL COMMENT '主键',
`jj_code` VARCHAR ( 36 ) DEFAULT NULL COMMENT '代码',
`jj_name` VARCHAR ( 36 ) DEFAULT NULL COMMENT '名称',
`riqi` VARCHAR ( 64 ) DEFAULT NULL COMMENT '日期',
`dwjz` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '单位净值',
`ljjz` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '累计净值',
`zdf` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '涨跌幅',
`mmfe` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '买卖份额',
`mmjz` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '买卖净值',
`mmje` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '买卖金额',
`pjcb` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '平均成本',
`comments` VARCHAR ( 5000 ) DEFAULT NULL COMMENT '备注',
PRIMARY KEY ( `id` ) USING BTREE 
) ENGINE = INNODB DEFAULT CHARSET = utf8;

alter table jj_history add column  `ly` varchar(36) DEFAULT NULL COMMENT  '来源';
alter table jj_history add column  `create_date` datetime DEFAULT NULL COMMENT '创建日期';

```



```sql
DROP TABLE IF EXISTS `jj_handle`;
CREATE TABLE `jj_handle` (
`id` VARCHAR ( 36 ) NOT NULL COMMENT '主键',
`riqi` VARCHAR ( 36 ) DEFAULT NULL COMMENT '日期',
`mrje` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '买入金额',
`mcfe` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '卖出份额',
`ccfe` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '持仓份额',
`cccb` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '持仓成本',
`t_type` VARCHAR ( 36 ) DEFAULT NULL COMMENT '买卖类型',
`comments` VARCHAR ( 5000 ) DEFAULT NULL COMMENT '备注',
PRIMARY KEY ( `id` ) USING BTREE 
) ENGINE = INNODB DEFAULT CHARSET = utf8;
```



