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


alter table jj_history add column `g1` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '上轨';
alter table jj_history add column `g2` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '中轨';
alter table jj_history add column `g3` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '下轨';
alter table jj_history add column `s1` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '数据1';
alter table jj_history add column `s2` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '数据2';
alter table jj_history add column `s3` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '数据3';
alter table jj_history add column `lnz` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '量能柱';
alter table jj_history add column `gwvyx` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '高位止盈线';
alter table jj_history add column `dwjcx` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '低位加仓线';
alter table jj_history add column `ypck` VARCHAR ( 36 ) DEFAULT NULL COMMENT '研判参考';

```


#### 操作表

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


#### BOLL策略表(弃用)

```sql
CREATE TABLE `jj_boll` (
`id` VARCHAR ( 36 ) NOT NULL COMMENT '主键',
`jj_code` VARCHAR ( 36 ) DEFAULT NULL COMMENT '代码',
`riqi` VARCHAR ( 64 ) DEFAULT NULL COMMENT '日期',
`g1` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '上轨',
`g2` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '中轨',
`g3` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '下轨',
`s1` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '数据1',
`s2` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '数据2',
`s3` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '数据3',
`lnz` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '量能柱',
`gwvyx` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '高位止盈线',
`dwjcx` DECIMAL ( 32, 9 ) DEFAULT NULL COMMENT '低位加仓线',
`ypck` VARCHAR ( 36 ) DEFAULT NULL COMMENT '研判参考',
`comments` VARCHAR ( 5000 ) DEFAULT NULL COMMENT '备注',
PRIMARY KEY ( `id` ) USING BTREE 
) ENGINE = INNODB DEFAULT CHARSET = utf8;

```


## BOLL策略

### 更新中轨
> 中轨 = 20日均线
#### 创建更新中轨函数
> 传入参数：jj_code
```sql
CREATE DEFINER=`root`@`localhost` FUNCTION `boll_g2`(jj_code_in VARCHAR(36)) RETURNS varchar(36) CHARSET utf8
    DETERMINISTIC
BEGIN

with temp as (
select (@i:=@i+1) as rownum,a.* from jj_history a,(SELECT @i:=0) as init
where a.jj_code = jj_code_in
ORDER BY a.riqi desc
) 
update jj_history u set u.g2 = (
select (select avg(t2.dwjz)  from temp t2
where t2.rownum >= t.rownum
and t2.rownum < t.rownum + 20
) as ma from temp t
where t.jj_code = jj_code_in
and t.riqi = u.riqi
) where u.jj_code = jj_code_in;

RETURN 'BOLL-中轨更新成功';

END

```

#### 调用函数
```sql
select boll_g2('000961')
```


### 更新数据1
> 数据1 = (净值-中轨)的平方
```sql
update jj_history set s1 = POWER((dwjz - g2),2)
```

### 更新数据2
> 数据2 = 数据1的20日均线

#### 创建函数
```sql
CREATE DEFINER=`root`@`localhost` FUNCTION `boll_s2`(jj_code_in VARCHAR(36)) RETURNS varchar(36) CHARSET utf8
    DETERMINISTIC
BEGIN

with temp as (
select (@i:=@i+1) as rownum,a.* from jj_history a,(SELECT @i:=0) as init
where a.jj_code = jj_code_in
ORDER BY a.riqi desc
) 
update jj_history u set u.s2 = (
select (select avg(t2.s1)  from temp t2
where t2.rownum >= t.rownum
and t2.rownum < t.rownum + 20
) as ma from temp t
where t.jj_code = jj_code_in
and t.riqi = u.riqi
) where u.jj_code = jj_code_in;

RETURN 'BOLL-数据2更新成功';

END

```

#### 调用函数
```sql

select boll_s2('000961')

```

### 更新数据3
> 数据3=数据2的平方根
```sql
update jj_history set s3 = SQRT(s2)
```

### 更新上轨
> 上轨 = 中轨+2*数据3

```sql
update jj_history set g1 = g2 + 2 * s3

```

### 更新下轨
> 下轨 = 中轨-2*数据3

```sql
update jj_history set g3 = g2 - 2 * s3

```

### 更新量能柱
> 量能柱 =(2*净值-上轨-下轨)/净值
```sql
update jj_history set lnz = (2*dwjz-g1-g3)/dwjz

```

### 更新高位止盈线
> 高位止盈线 = 中轨 + (上轨 - 中轨) * 0.309

```sql
update jj_history set gwvyx = g2 + (g1 - g2) * 0.309

```

### 更新低位加仓线
> 低位加仓线 = 中轨 + (中轨 - 下轨) * 0.309

```sql
update jj_history set dwjcx = g2 - (g2 - g3) * 0.309

```



### 更新研判参考
#### 创建函数
```sql
CREATE DEFINER=`root`@`localhost` FUNCTION `boll_ypck`(jj_code_in VARCHAR(36)) RETURNS varchar(36) CHARSET utf8
    DETERMINISTIC
BEGIN

with temp as (
select (@i:=@i+1) as rownum,a.* from jj_history a,(SELECT @i:=0) as init
where a.jj_code = jj_code_in
ORDER BY a.riqi desc
) 

update jj_history u set u.ypck = (
select 
CASE 
	WHEN zt.dwjz > zt.g1 and jt.dwjz < jt.g1 THEN
		"清仓"
	WHEN zt.dwjz > zt.gwvyx and zt.dwjz < zt.g1 and jt.dwjz < jt.gwvyx THEN
		"止盈赎回"
	WHEN jt.dwjz > jt.dwjcx THEN
		"观望期"
	WHEN jt.dwjz > jt.g3 THEN
		"可加仓"
	ELSE
		"探底加仓"
END 
from temp jt
left join temp zt on zt.jj_code = jj_code_in
and zt.rownum = jt.rownum + 1
where jt.jj_code = jj_code_in
and jt.riqi = u.riqi

) where u.jj_code = jj_code_in;

RETURN 'BOLL-研判参考更新成功';

END

```

#### 调用函数
```sql
select boll_ypck('000961')
```


