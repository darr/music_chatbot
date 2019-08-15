
```shell
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.3.2.deb
sudo dpkg -i elasticsearch-6.3.2.deb
```

打开 /etc/elasticsearch/elasticsearch.yml

```shell
sudo vim /etc/elasticsearch/elasticsearch.yml
```

编辑 此行

```shell
# network.host: 192.168.0.1
```

取消注释并将IP设置为服务器地址：

```shell
network.host: 192.168.4.105  #我的局域网地址是这个
```

保存并退出该文件

最后，启动并使用Elasticsearch 服务。

```shell
sudo systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service
```

通过浏览器验证是否一切正常：

```shell
http://192.168.4.105:9200/
```

返回

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

返回

```shell
epoch      timestamp cluster       status node.total node.data shards pri relo init unassign pending_tasks max_task_wait_time active_shards_percent
1565753263 11:27:43  elasticsearch green           1         1      0   0    0    0        0             0                  -                100.0%
```

接下来我们安装Kibana，它将为我们提供图形化前端。
安装Kibana

与安装 Elasticsearch 方式相同

```shell
wget https://artifacts.elastic.co/downloads/kibana/kibana-6.3.2-amd64.deb
sudo dpkg -i kibana-6.3.2-amd64.deb
```

打开 /etc/kibana/kibana.yml 

```shell
sudo vim /etc/kibana/kibana.yml
```

更新一下两行,必要时取消注释

```shell
server.host: "192.168.4.105"
elasticsearch.url: "http://192.168.4.105:9200"
```

保存并退出

配置JVM的VM堆大小

```shell
sudo sysctl -w vm.max_map_count=262144
```

启动 并使用 Kibana服务

```shell
sudo systemctl enable kibana.service
sudo systemctl start kibana.service
```

打开下面的网址

```shell
http://192.168.4.105:5601
```

进入kibana

下面安装 Logstash

```shell
wget https://artifacts.elastic.co/downloads/logstash/logstash-6.3.2.deb
sudo dpkg -i logstash-6.3.2.deb
```

进入 /etc/logstash/logstash.yml

```shell
sudo vim /etc/logstash/logstash.yml
```

修改

```shell
http.host: "192.168.4.105"
```

启动并使用Logstash服务

```shell
sudo systemctl enable logstash.service
sudo systemctl start logstash.service
```

## 安装 FileBeats

首先，进入logstash安装目录

```shell
cd /usr/share/logstash/
```

运行下面命令，安装FileBeats Logstash 插件

```shell
sudo bin/logstash-plugin install logstash-input-beats
```
output
```shell
Validating logstash-input-beats
Installing logstash-input-beats
Installation successful
```

配置Logstash以接收FileBeat 数据
创建 /etc/logstash/conf.d/beats.conf 并添加以下内容。

```shell
input {
  beats {
    port => "5044"
  }
}
output {
  elasticsearch {
    hosts => ["192.168.4.105:9200"]
    manage_template => false
    index => "%{[@metadata][beat]}-%{[@metadata][version]}-%{+YYYY.MM.dd}"
  }
}

```

请务必在主机hosts中设置实际的地址。 保存并退出文件。

## 发送日志

下面将配置Elasticsearch 服务器以发送日志，演示如何配置系统以将日志发送到服务器。

如果要配置从其他服务器发送日志，需在其他服务器上执行以下步骤。


首先，下载并安装FileBeat代理。
```shell
wget https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-6.3.2-amd64.deb
sudo dpkg -i filebeat-6.3.2-amd64.deb
```
接下来我们需要配置它。

打开/etc/filebeat/filebeat.yml

```shell
filebeat.prospectors:
- input_type: log
  paths:
    - /var/log/*/*.log

output.logstash:
  hosts: ["192.168.4.15:5044"]
```

启动并使用FileBeat 服务
```shell
sudo systemctl enable filebeat.service
sudo systemctl start filebeat.service
```
最后我们将FileBeat模版安装到Kibana。如果使用FileBeat为多哥服务器设置日志记录，
则只需要执行一次此操作。  

```shell
sudo filebeat setup --template -E output.logstash.enabled=false -E 'output.elasticsearch.hosts=["192.168.4.105:9200"]'
```

output
```shell
Exiting: prospectors and inputs used in the configuration file, define only inputs not both
```
这可能是因为刚才设置的 filebeat.prospectors
把这些设置删除，尝试

```shell
sudo filebeat setup --template -E output.logstash.enabled=false -E 'output.elasticsearch.hosts=["192.168.4.105:9200"]'

```

output
```shell
Loaded index template
```

等待几分钟让日志最终进入Elasticsearch，然后回到Kibana

等待后并没有成功

测试了elasticsearch 和kibana 可以工作
问题应该处在FileBeat 或者 Logstash
由于我的项目并不是收集日志，而只是使用elasticsearch 数据库。  
所以只是测试到这里，Logstash和FileBeat并没有调通。


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

