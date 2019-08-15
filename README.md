# MusicChatbot

chatbot based on music region using method including es and music kb.  
基于14W歌曲知识库的问答尝试，功能包括歌词接龙，已知歌词找歌曲以及歌曲歌手歌词三角关系的问答。  

# install elasticsearch

download and install elasticsearch

```shell
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.3.2.deb
sudo dpkg -i elasticsearch-6.3.2.deb
```

open /etc/elasticsearch/elasticsearch.yml

```shell
sudo vim /etc/elasticsearch/elasticsearch.yml
```

edit this line

```shell
# network.host: 192.168.0.1
```

set your own device IP address

```shell
network.host: 192.168.4.105
```
save and quit

start and use Elasticsearch service.

```shell
sudo systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service
```

check if the elasticsearch can work

```shell
http://192.168.4.105:9200/
```
return

```shell
{
  "name" : "fOiX2mX",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "ocKdE7cfT1C_gSOpfYLLMw",
  "version" : {
    "number" : "6.3.2",
    "build_flavor" : "default",
    "build_type" : "deb",
    "build_hash" : "053779d",
    "build_date" : "2018-07-20T05:20:23.451332Z",
    "build_snapshot" : false,
    "lucene_version" : "7.3.1",
    "minimum_wire_compatibility_version" : "5.6.0",
    "minimum_index_compatibility_version" : "5.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

```shell
http://192.168.4.105:9200/_cat/health?v
```

return

```shell
epoch      timestamp cluster       status node.total node.data shards pri relo init unassign pending_tasks max_task_wait_time active_shards_percent
1565753263 11:27:43  elasticsearch green           1         1      0   0    0    0        0             0                  -                100.0%
```
# install kibana (optional)

```shell
wget https://artifacts.elastic.co/downloads/kibana/kibana-6.3.2-amd64.deb
sudo dpkg -i kibana-6.3.2-amd64.deb
```

open /etc/kibana/kibana.yml 

```shell
sudo vim /etc/kibana/kibana.yml
```

set 

```shell
server.host: "192.168.4.105"
elasticsearch.url: "http://192.168.4.105:9200"
```
save and quit.

config JVM VM  

```shell
sudo sysctl -w vm.max_map_count=262144
```

start and use Kibana service

```shell
sudo systemctl enable kibana.service
sudo systemctl start kibana.service
```
check if kibana can work

```shell
http://192.168.4.105:5601
```

# install ik

Install ik for Chinese segment.

First move to elasticsearch installed fold.
Most commonly is:

```shell
cd /usr/share/elasticsearch
```
My device is Ubuntu.
Then install ik plugin

```shell
sudo ./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v6.3.2/elasticsearch-analysis-ik-6.3.2.zip
```
Use 6.3.2, because my elasticsearch version is 6.3.2

# unzip music.json.zip

music.json.zip is at ./data/

```shell
unzip music.json.zip
```

# change file etc.py

change
ES_IP = you device address
like 192.168.4.105

# How to run?

```shell
bash run.sh
```

This command will create the environment that needed by the models.  
This project is created on the purposes of easy-on-run.  
If you want to know the details about the models, just read code.  

# reusult

```shell
请问这句歌词的上下句：
好好的一份爱啊怎么会慢慢变坏
下一句：
暖暖的眼泪跟寒雨混成一块  ---来自刘德华的《冰雨》
冷冷的冰雨在脸上胡乱的拍  ---来自高胜美的《寒星》
冷冷的冰雨在脸上胡乱的拍  ---来自刘德华的《一段情》
上一句：
两个人却有不同无奈  ---来自刘德华的《冰雨》
两个人却有不同无奈  ---来自高胜美的《寒星》
两个人却有不同无奈  ---来自刘德华的《一段情》
请问这句歌词的上下句：
匆匆上路
下一句：
末敢怠慢  ---来自福山雅治的《向日葵》
末敢怠慢  ---来自邓丽君的《向日葵》
上一句：
自苦没时间  ---来自福山雅治的《向日葵》
自苦没时间  ---来自邓丽君的《向日葵》
请问这句歌词的上下句：
想要说声爱你
下一句：
却被吹散在风里  ---来自苏云的《大海》
却被吹散在风里  ---来自梦想星搭档的《大海》
却被吹散在风里  ---来自杨培安的《大海》
却被吹散在风里  ---来自阿宝的《大海》
却被吹散在风里  ---来自张雨生的《大海》
上一句：
每朵浪花记清  ---来自苏云的《大海》
徒劳无功想把每朵浪花记清  ---来自梦想星搭档的《大海》
想把每朵浪花记起  ---来自杨培安的《大海》
想把每朵浪花记清  ---来自阿宝的《大海》
想把每朵浪花记清  ---来自张雨生的《大海》
请问这句歌词的上下句：
原谅我这一生不羁放纵爱自由
下一句：
也会怕有一天会跌倒  ---来自我是歌手的《海阔天空》
也会怕有一天会跌倒  ---来自左右乐队的《海阔天空》
也会怕有一天会跌倒  ---来自BEYOND的《海阔天空》
也会怕有一天会跌倒  ---来自DJMAX的《고백& 꽃 늑대 Part 2 》
也会怕有一天会跌倒  ---来自beyond的《海阔天空》
也会怕有一天会跌倒  ---来自黄秋生的《海阔天空》
也会怕有一天  ---来自夜山明的《致家驹》
也会怕有一天会跌倒 WOONO  ---来自庞锟的《光辉BEYOND》
也会怕有一天会跌倒OH NO  ---来自许云上的《海阔天空》
上一句：
(谁明白我)  ---来自我是歌手的《海阔天空》
心里爱(谁明白我)  ---来自左右乐队的《海阔天空》
心里爱(谁明白我)  ---来自BEYOND的《海阔天空》
心里爱(谁明白我)  ---来自DJMAX的《고백& 꽃 늑대 Part 2 》
心里爱(谁明白我)  ---来自beyond的《海阔天空》
心里爱(谁明白我)  ---来自黄秋生的《海阔天空》
总会想起你  ---来自夜山明的《致家驹》
问谁又能做到  ---来自庞锟的《光辉BEYOND》
可会变  ---来自许云上的《海阔天空》
请问这句歌词的上下句：
狼烟起江山北望
下一句：
龙起卷马长嘶剑气如霜  ---来自名杂牌精选的《精忠报国屠洪纲》
上一句：
精忠报国  ---来自名杂牌精选的《精忠报国屠洪纲》
```

# 项目由来
听歌识曲，歌词对唱，智能点歌是目前智能音乐中特别火的方向。  
本项目将使用最为传统的方法，以构建歌曲歌词语料库出发，以歌词为中心，构建歌曲、歌手、歌词三角知识库。并借助es完成相应的查询服务。  
本项目的技术点包括：  
1、歌曲知识库构建  
2、es搜索  

本项目尝试完成的工作：  
1、歌词问答  
2、已知歌词查歌曲  
3、歌曲知识问答  

# 项目步骤:  
1、歌词语料库构建  
2、歌词、歌曲、歌手知识库构建  
3、基于知识库的问答挖掘  

# 项目路线图
![image](./img/route.png)  

# 总结
１）本项目是对es的一个简单应用，es用的精确匹配。  
