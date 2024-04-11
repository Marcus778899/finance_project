use finance;
show tables;
select * from stock_price order by stock_id ,Date ASC;
select * from finance_statement where stock_id = '2330';
select * from basic_information;
show create table basic_information;
truncate table basic_information;
