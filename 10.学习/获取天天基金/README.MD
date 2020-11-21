
# 前言

1. 基金实时信息：`http://fundgz.1234567.com.cn/js/001186.js?rt=1463558676006`

001186为基金代号

返回值：jsonpgz({“fundcode”:“001186”,“name”:“富国文体健康股票”,“jzrq”:“2016-05-17”,“dwjz”:“0.7420”,“gsz”:“0.7251”,“gszzl”:"-2.28",“gztime”:“2016-05-18 15:00”});


2. 基金详细信息：`http://fund.eastmoney.com/pingzhongdata/001186.js?v=20160518155842`

数据量太大不贴了

还有两个

3. 所有基金名称列表代码: `http://fund.eastmoney.com/js/fundcode_search.js`


4. 所有基金公司名称列表代码: `http://fund.eastmoney.com/js/jjjz_gs.js?dt=1463791574015`

5. 查看基金历史净值: `http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery183006797018539211241_1593855325551&fundCode=004070&pageIndex=1&pageSize=20&startDate=2020-06-01&endDate=2020-07-01&_=1593857119095`

# 建表
```sql
CREATE TABLE `jj_info` (
`jj_code` VARCHAR ( 36 ) NOT NULL COMMENT '代码',
`jj_name` VARCHAR ( 36 ) DEFAULT NULL COMMENT '名称',
`jj_type` VARCHAR ( 36 ) DEFAULT NULL COMMENT '类型',
`jj_base_info` VARCHAR ( 10000 ) DEFAULT NULL COMMENT '备注',
PRIMARY KEY ( `jj_code` ) USING BTREE 
) ENGINE = INNODB DEFAULT CHARSET = utf8;
```

# 数据处理
## 查询评分高的基金
```sql
with temp as (
SELECT
substring_index(substring(i.jj_base_info,locate('workTime":"',i.jj_base_info)+LENGTH('workTime":"')),'"',1) as workTime,		
substring_index(substring(i.jj_base_info,locate('Data_performanceEvaluation = {"avr":"',i.jj_base_info)+LENGTH('Data_performanceEvaluation = {"avr":"')),'"',1) as j_avr,		
substring_index(substring(i.jj_base_info,locate('power":{"avr":"',i.jj_base_info)+LENGTH('power":{"avr":"')),'"',1) as p_avr,
substring_index(substring(i.jj_base_info,locate('jpg","name":"',i.jj_base_info)+LENGTH('jpg","name":"')),'"',1) as p_name,
substring_index(substring(i.jj_base_info,locate('"fundSize":"',i.jj_base_info)+LENGTH('"fundSize":"')),'"',1) as fundSize,
	i.*
FROM
	jj_info i 
WHERE
	i.jj_type NOT IN ( '债券型', '定开债券', '固定收益', '债券指数' , 'ETF-场内'  )
)
select 
t.jj_code as '基金代码',
t.jj_name as '基金名称',
t.jj_type as '基金类型',
t.j_avr as '基金评分',
t.p_name as '基金经理',
t.workTime as '从业时间',
t.p_avr as '基金经理评分'
,t.fundSize as '管理规模'
from temp t
where t.workTime >= 3
and t.j_avr >= 70 and t.j_avr <= 100
and t.p_avr >= 70 and t.p_avr <= 100
```
![在这里插入图片描述](https://images.gitee.com/uploads/images/2020/0704/233852_2953ea4d_1542471.png)


## 查询所有基金持仓最高的股票
```sql
with temp as (
select * from (
SELECT
i.jj_code,
i.jj_name,
substring_index( substring_index( substring( i.jj_base_info, locate( '股票占净比', i.jj_base_info ) + LENGTH( '股票占净比' ) ), ']', 1 ), ',', -1 ) as gprate,
replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"','') as code,
substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',1) AS code1	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',2),',',-1) AS code2	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',3),',',-1) AS code3	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',4),',',-1) AS code4	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',5),',',-1) AS code5	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',6),',',-1) AS code6	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',7),',',-1) AS code7	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',8),',',-1) AS code8	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',9),',',-1) AS code9	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',10),',',-1) AS code10
FROM
	jj_info i 
WHERE
	i.jj_type IN ( '混合型', '股票型')
) h
where h.code1 <> h.code10
and h.code <> ''
and h.gprate > 60
	) 
select 
al.code1,
count(1) con
from (
select t.code1 from temp t
UNION all
select t.code2 from temp t
UNION all
select t.code3 from temp t
UNION all
select t.code4 from temp t
UNION all
select t.code5 from temp t
UNION all
select t.code6 from temp t
UNION all
select t.code7 from temp t
UNION all
select t.code8 from temp t
UNION all
select t.code9 from temp t
UNION all
select t.code10 from temp t
) al
GROUP BY
al.code1
HAVING count(1) > 170



```

## 查询以上股票的基金
```SQL
with temp as (
select * from (
SELECT
i.jj_code,
i.jj_name,
substring_index( substring_index( substring( i.jj_base_info, locate( '股票占净比', i.jj_base_info ) + LENGTH( '股票占净比' ) ), ']', 1 ), ',', -1 ) as gprate,
replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"','') as code,
substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',1) AS code1	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',2),',',-1) AS code2	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',3),',',-1) AS code3	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',4),',',-1) AS code4	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',5),',',-1) AS code5	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',6),',',-1) AS code6	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',7),',',-1) AS code7	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',8),',',-1) AS code8	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',9),',',-1) AS code9	,
substring_index(substring_index(replace(substring_index( substring( i.jj_base_info, locate( 'stockCodes=[', i.jj_base_info ) + LENGTH( 'stockCodes=[' ) ), ']', 1 ),'"',''),',',10),',',-1) AS code10
FROM
	jj_info i 
WHERE
	i.jj_type IN ( '混合型', '股票型')
) h
where h.code1 <> h.code10
and h.code <> ''
and h.gprate > 60
	)
select te.* from temp te
where 
te.code1 in ('0024752','3000592','0025552','6005701','6010121','6000361','3000142','6005191','0008582','6018881','6008871','0006512','6000301','6002761','3007602','0003332','6013181','3007502','6032591','0006612')
and te.code2 in ('0024752','3000592','0025552','6005701','6010121','6000361','3000142','6005191','0008582','6018881','6008871','0006512','6000301','6002761','3007602','0003332','6013181','3007502','6032591','0006612')
and te.code3 in ('0024752','3000592','0025552','6005701','6010121','6000361','3000142','6005191','0008582','6018881','6008871','0006512','6000301','6002761','3007602','0003332','6013181','3007502','6032591','0006612')
and te.code4 in ('0024752','3000592','0025552','6005701','6010121','6000361','3000142','6005191','0008582','6018881','6008871','0006512','6000301','6002761','3007602','0003332','6013181','3007502','6032591','0006612')
and te.code5 in ('0024752','3000592','0025552','6005701','6010121','6000361','3000142','6005191','0008582','6018881','6008871','0006512','6000301','6002761','3007602','0003332','6013181','3007502','6032591','0006612')
and te.code6 in ('0024752','3000592','0025552','6005701','6010121','6000361','3000142','6005191','0008582','6018881','6008871','0006512','6000301','6002761','3007602','0003332','6013181','3007502','6032591','0006612')
and te.code7 in ('0024752','3000592','0025552','6005701','6010121','6000361','3000142','6005191','0008582','6018881','6008871','0006512','6000301','6002761','3007602','0003332','6013181','3007502','6032591','0006612')
and te.code8 in ('0024752','3000592','0025552','6005701','6010121','6000361','3000142','6005191','0008582','6018881','6008871','0006512','6000301','6002761','3007602','0003332','6013181','3007502','6032591','0006612')
and te.code9 in ('0024752','3000592','0025552','6005701','6010121','6000361','3000142','6005191','0008582','6018881','6008871','0006512','6000301','6002761','3007602','0003332','6013181','3007502','6032591','0006612')
and te.code10 in ('0024752','3000592','0025552','6005701','6010121','6000361','3000142','6005191','0008582','6018881','6008871','0006512','6000301','6002761','3007602','0003332','6013181','3007502','6032591','0006612')
```