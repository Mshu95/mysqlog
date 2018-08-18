# mysqlog
根据mysql二进制日志文件，提取sql语句，以及回滚sql语句，人性化显示操作记录
>案发当天，中午2点的天气很是炎热，知了拼命的鸣叫，仿佛要和天气叫板，公司的老空调还算没有拖后腿，整个工作区温度适宜，我在整理一批刚结束的爬虫数据，一切都是那么正常，毫无征兆。

复制sql语句，修改表名、列名，run~

**次奥 ！**2.03s 删除了10万数据，数据虽然不多但是爬的辛苦啊，顿时感觉天气燥热，浑身是汗，呼吸困难，什么也不想干，就想骂人；

一直以为这种事情不会发生在我身上，对于数据回滚的知识也一直是片空白，现在终于明白了，哪个CTO年轻的时候没有删过几个库，没干过这种蠢事说明你还 So Young；

   扯止。

-----------------------------------------------------

使用事务安全操作
========


> 始于 BEGIN; 终于 ROLLBACK / COMMIT;

 1. 啥也别说运行一次BEGIN; 
 2. 执行增/删/改sql语句，然后使用select查看是否操作正确；
 3. 如果正确运行一次COMMIT; 否则运行一次ROLLBACK;

举个栗子🌰🐿️
----

操作之前的数据：
    SELECT * from sys_user where id = 2 ;
    结果：2	123456 mshu 123456  11855079819 2018-04-30 11:41:03  无不良记录	100	100
ROLLBACK；  使用  
    BEGIN;
    DELETE FROM sys_user where id = 2;
    SELECT * from sys_user where id = 2 ;
    结果：
    ROLLBACK;
    SELECT * from sys_user where id = 2 ;
    结果：2	123456 mshu 123456  11855079819 2018-04-30 11:41:03  无不良记录	100	100
 COMMIT; 使用
    BEGIN;
    DELETE FROM sys_user where id = 2;
    SELECT * from sys_user where id = 2 ;
    结果：
    COMMIT;
    SELECT * from sys_user where id = 2 ;
    结果：
    

> 人都是懒惰的，每次操作sql,都要运行BEGIN；ROLLBACK / COMMIT实在太麻烦，当遇到概率事件时，人们往往会把有利于自己的一边的概率放大。                    ——Mshu

Mysql是有日志记录功能的，但是默认关闭，就像著名哲学家Mshu说的那样，Mysql也认为误操作是个概率事件，如果记录操作日志的话，时间久、频率高就会需要很大的空间，而且用不到的话就是一堆垃圾，所以它放小了不利自己的概率，认为没有必要开启。

*我猜我在这里鬼扯让读者感到很无聊，但是我真的觉得在这里扯很舒服，所以我认为这篇文章被人读到的概率也很小。*

为了保证文章顺利发表，言归正传

开启logbin
========

使用MySQL的日志记录功能，首先要确定是否开启了logbin，mysq命令：

    show variables like '%log_bin%' 
结果：
Variable|value
---|:--|
log_bin|	ON
sql_log_bin	|ON
log_bin_basename|C:\ProgramData\MySQL\MySQL Server 5.7\Data\mysql-log  
log_bin_index	|C:\ProgramData\MySQL\MySQL Server 5.7\Data\mysql-log.index

很欣慰的看到我已经开启了logbin😊；

**怎么开启？**

如果没有开启需要修改my.ini文件，至于这个文件在哪，Linux当然使用whereis,
Window的话，还是MySQL命令：
    show variables like '%data%' 
结果：
Variable|value
---|:--|
datadir|	C:\ProgramData\MySQL\MySQL Server 5.7\Data\

就在这个目录的父目录下。

**怎么修改？**

加菊花，呸，加句话：log-bin=mysql-log
    # Binary Logging.
    # log-bin
    log-bin=mysql-log
等号后面随便取，这将会是你的日志文件名，如我所取mysql-log

**重启服务器**

重启之后操作一番增删改后，可以看到日志文件，目录就在`show variables like '%data%'`显示的 datadir指向的文件夹里
    文件名为你刚刚设置的名字加00000加数字的二进制文件
    如：mysql-log.000001
这就是MySQL的日志文件。

**针对日志文件show一波命令**

---|:--|
 flush logs |	至此生成新的日志文件
reset master| 清空日志文件


听说在此之前需要保证两个设置是对的

 1. 存储引擎：InnoDB
 2. 日志格式：ROW
由于我的MySQL默认都是对的，我就没有测试，就简单介绍一下吧：

查看存储引擎
    show engines;
查看日志格式
    show variables like '%binlog_format%';
    

mysqlog
=======
**怎么阅读日志文件？**

>下面开始画重点，这也是我写这篇文章的重要目的
既然日志文件是二进制，怎么使用呢，感兴趣的小伙伴可以了解一下**`mysqlbinlog`命令**，这里不做重点；
重点是我写的一个小工具，使用简单，操作流畅，令人心旷神怡。

**功能介绍：**根据MySQL二进制日志文件，生成人类可以理解的操作记录文件，以excel人性化呈现；
而你只需要提供二进制文件以及数据库ip、用户名、和密码即可
项目使用python3开发，所以你电脑要安装python；


**使用步骤：**

 1. /log0000/文件夹内放你要解析的二进制日志文件
 2. 在main.py文件中填入config配置（数据库ip、用户名、和密码）
 3. 运行主方法，在/result/文件下可得到解析结果。
**运行结果：**

包含时间、增删改的类型且用不同颜色区分明显，数据库，表，需要回滚的sql语句，以及当时执行的语句；一目了然。

本工具主要是用来解析mysql的操作日志，除了生成当时执行的sql语句外，还有为了数据回滚的sql语句，都是标准的sql,可以直接复制运行。给使用者来分析和回滚，我把它命名为**[mysqlog][1]**，<---链接为GitHub地址。

数据回滚很重要，误删数据别哭闹。
MySQLog福带到，让你眉开又眼笑。
好言相劝若不理，删库跑路就是你。

免责声明
----
本项目作者放荡不羁，不能保证项目准确无误，数据无价，对于生成的sql，请适当检查后使用。

  [1]: https://github.com/Mshu95/mysqlog