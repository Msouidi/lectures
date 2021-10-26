# Install elastic stack

## 1. Setup the infrastructure
```
git clone git@github.com:msouidi/lectures.git
cd elastic
vagrant up
```
## 2. Setup logstash
Create a configuration file `called 02-beats-input.conf` where you will set up your Filebeat input:
```
sudo nano /etc/logstash/conf.d/02-beats-input.conf
```
Insert the following input configuration. This specifies a beats input that will listen on TCP port 5044.
```
input {
  beats {
    port => 5044
  }
}
```
Save and close the file. Next, create a configuration file called `10-syslog-filter.conf`, where we will add a filter for system logs, also known as syslogs:
```
sudo nano /etc/logstash/conf.d/10-syslog-filter.conf
```
Insert the following syslog filter configuration. This example system logs configuration was taken from official Elastic documentation. This filter is used to parse incoming system logs to make them structured and usable by the predefined Kibana dashboards:
```
filter {
  if [fileset][module] == "system" {
    if [fileset][name] == "auth" {
      grok {
        match => { "message" => ["%{SYSLOGTIMESTAMP:[system][auth][timestamp]} %{SYSLOGHOST:[system][auth][hostname]} sshd(?:\[%{POSINT:[system][auth][pid]}\])?: %{DATA:[system][auth][ssh][event]} %{DATA:[system][auth][ssh][method]} for (invalid user )?%{DATA:[system][auth][user]} from %{IPORHOST:[system][auth][ssh][ip]} port %{NUMBER:[system][auth][ssh][port]} ssh2(: %{GREEDYDATA:[system][auth][ssh][signature]})?",
                  "%{SYSLOGTIMESTAMP:[system][auth][timestamp]} %{SYSLOGHOST:[system][auth][hostname]} sshd(?:\[%{POSINT:[system][auth][pid]}\])?: %{DATA:[system][auth][ssh][event]} user %{DATA:[system][auth][user]} from %{IPORHOST:[system][auth][ssh][ip]}",
                  "%{SYSLOGTIMESTAMP:[system][auth][timestamp]} %{SYSLOGHOST:[system][auth][hostname]} sshd(?:\[%{POSINT:[system][auth][pid]}\])?: Did not receive identification string from %{IPORHOST:[system][auth][ssh][dropped_ip]}",
                  "%{SYSLOGTIMESTAMP:[system][auth][timestamp]} %{SYSLOGHOST:[system][auth][hostname]} sudo(?:\[%{POSINT:[system][auth][pid]}\])?: \s*%{DATA:[system][auth][user]} :( %{DATA:[system][auth][sudo][error]} ;)? TTY=%{DATA:[system][auth][sudo][tty]} ; PWD=%{DATA:[system][auth][sudo][pwd]} ; USER=%{DATA:[system][auth][sudo][user]} ; COMMAND=%{GREEDYDATA:[system][auth][sudo][command]}",
                  "%{SYSLOGTIMESTAMP:[system][auth][timestamp]} %{SYSLOGHOST:[system][auth][hostname]} groupadd(?:\[%{POSINT:[system][auth][pid]}\])?: new group: name=%{DATA:system.auth.groupadd.name}, GID=%{NUMBER:system.auth.groupadd.gid}",
                  "%{SYSLOGTIMESTAMP:[system][auth][timestamp]} %{SYSLOGHOST:[system][auth][hostname]} useradd(?:\[%{POSINT:[system][auth][pid]}\])?: new user: name=%{DATA:[system][auth][user][add][name]}, UID=%{NUMBER:[system][auth][user][add][uid]}, GID=%{NUMBER:[system][auth][user][add][gid]}, home=%{DATA:[system][auth][user][add][home]}, shell=%{DATA:[system][auth][user][add][shell]}$",
                  "%{SYSLOGTIMESTAMP:[system][auth][timestamp]} %{SYSLOGHOST:[system][auth][hostname]} %{DATA:[system][auth][program]}(?:\[%{POSINT:[system][auth][pid]}\])?: %{GREEDYMULTILINE:[system][auth][message]}"] }
        pattern_definitions => {
          "GREEDYMULTILINE"=> "(.|\n)*"
        }
        remove_field => "message"
      }
      date {
        match => [ "[system][auth][timestamp]", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss" ]
      }
      geoip {
        source => "[system][auth][ssh][ip]"
        target => "[system][auth][ssh][geoip]"
      }
    }
    else if [fileset][name] == "syslog" {
      grok {
        match => { "message" => ["%{SYSLOGTIMESTAMP:[system][syslog][timestamp]} %{SYSLOGHOST:[system][syslog][hostname]} %{DATA:[system][syslog][program]}(?:\[%{POSINT:[system][syslog][pid]}\])?: %{GREEDYMULTILINE:[system][syslog][message]}"] }
        pattern_definitions => { "GREEDYMULTILINE" => "(.|\n)*" }
        remove_field => "message"
      }
      date {
        match => [ "[system][syslog][timestamp]", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss" ]
      }
    }
  }
}
```
Save and close the file when finished.

Lastly, create a configuration file called `30-elasticsearch-output.conf`:

```
sudo nano /etc/logstash/conf.d/30-elasticsearch-output.conf
```
Insert the following output configuration. Essentially, this output configures Logstash to store the Beats data in Elasticsearch, which is running at `localhost:9200`, in an index named after the Beat used. The Beat used in this tutorial is Filebeat:
```
output {
  elasticsearch {
    hosts => ["localhost:9200"]
    manage_template => false
    index => "%{[@metadata][beat]}-%{[@metadata][version]}-%{+YYYY.MM.dd}"
  }
}
```
Save and close the file.

If you want to add filters for other applications that use the Filebeat input, be sure to name the files so they’re sorted between the input and the output configuration, meaning that the file names should begin with a two-digit number between `02` and `30`.

Test your Logstash configuration with this command:
```
sudo -u logstash /usr/share/logstash/bin/logstash --path.settings /etc/logstash -t
```
If there are no syntax errors, your output will display `Configuration OK` after a few seconds. If you don’t see this in your output, check for any errors that appear in your output and update your configuration to correct them.

If your configuration test is successful, start and enable Logstash to put the configuration changes into effect:
```
sudo systemctl start logstash
sudo systemctl enable logstash
```
## 3. Setup Filebeat
In this tutorial we will use Filebeat to forward local logs to our Elastic Stack.
Configure Filebeat to connect to Logstash. Here, we will modify the example configuration file that comes with Filebeat.
```
sudo nano /etc/filebeat/filebeat.yml
```
Filebeat supports numerous outputs, but you’ll usually only send events directly to Elasticsearch or to Logstash for additional processing. In this tutorial, we’ll use Logstash to perform additional processing on the data collected by Filebeat. Filebeat will not need to send any data directly to Elasticsearch, so let’s disable that output. To do so, find the `output.elasticsearch` section and comment out the following lines by preceding them with a `#`:
```
...
#output.elasticsearch:
  # Array of hosts to connect to.
  #hosts: ["localhost:9200"]
...
```
Then, configure the `output.logstash` section. Uncomment the lines `output.logstash`: and `hosts: ["localhost:5044"]` by removing the #. This will configure Filebeat to connect to Logstash on your Elastic Stack server at port `5044`, the port for which we specified a Logstash input earlier:
```
output.logstash:
  # The Logstash hosts
  hosts: ["localhost:5044"]
```
Save and close the file.

The functionality of Filebeat can be extended with Filebeat modules. In this tutorial we will use the system module, which collects and parses logs created by the system logging service of common Linux distributions.

Let’s enable it:
```
sudo filebeat modules enable system
```
You can see a list of enabled and disabled modules by running:
```
sudo filebeat modules list
```
You will see a list similar to the following:
```
Output
Enabled:
system

Disabled:
apache2
auditd
elasticsearch
icinga
iis
kafka
kibana
logstash
mongodb
mysql
nginx
osquery
postgresql
redis
traefik
```
By default, Filebeat is configured to use default paths for the syslog and authorization logs. In the case of this tutorial, you do not need to change anything in the configuration. You can see the parameters of the module in the `/etc/filebeat/modules.d/system.yml` configuration file.

Next, load the index template into Elasticsearch. An Elasticsearch index is a collection of documents that have similar characteristics. Indexes are identified with a name, which is used to refer to the index when performing various operations within it. The index template will be automatically applied when a new index is created.

To load the template, use the following command:
```
sudo filebeat setup --template -E output.logstash.enabled=false -E 'output.elasticsearch.hosts=["localhost:9200"]'
```
```
Output
Loaded index template
```
Filebeat comes packaged with sample Kibana dashboards that allow you to visualize Filebeat data in Kibana. Before you can use the dashboards, you need to create the index pattern and load the dashboards into Kibana.

As the dashboards load, Filebeat connects to Elasticsearch to check version information. To load dashboards when Logstash is enabled, you need to disable the Logstash output and enable Elasticsearch output:
```
sudo filebeat setup -e -E output.logstash.enabled=false -E output.elasticsearch.hosts=['localhost:9200'] -E setup.kibana.host=localhost:5601
```
You will see output that looks like this:
```
Output
2018-09-10T08:39:15.844Z        INFO    instance/beat.go:273    Setup Beat: filebeat; Version: 7.6.1
2018-09-10T08:39:15.845Z        INFO    elasticsearch/client.go:163     Elasticsearch url: http://localhost:9200
2018-09-10T08:39:15.845Z        INFO    pipeline/module.go:98   Beat name: elk
2018-09-10T08:39:15.845Z        INFO    elasticsearch/client.go:163     Elasticsearch url: http://localhost:9200
2018-09-10T08:39:15.849Z        INFO    elasticsearch/client.go:708     Connected to Elasticsearch version 7.6.1
2018-09-10T08:39:15.856Z        INFO    template/load.go:129    Template already exists and will not be overwritten.
Loaded index template
Loading dashboards (Kibana must be running and reachable)
2018-09-10T08:39:15.857Z        INFO    elasticsearch/client.go:163     Elasticsearch url: http://localhost:9200
2018-09-10T08:39:15.865Z        INFO    elasticsearch/client.go:708     Connected to Elasticsearch version 7.6.1
2018-09-10T08:39:15.865Z        INFO    kibana/client.go:113    Kibana url: http://localhost:5601
2018-09-10T08:39:45.357Z        INFO    instance/beat.go:659    Kibana dashboards successfully loaded.
Loaded dashboards
2018-09-10T08:39:45.358Z        INFO    elasticsearch/client.go:163     Elasticsearch url: http://localhost:9200
2018-09-10T08:39:45.361Z        INFO    elasticsearch/client.go:708     Connected to Elasticsearch version 7.6.1
2018-09-10T08:39:45.361Z        INFO    kibana/client.go:113    Kibana url: http://localhost:5601
2018-09-10T08:39:45.455Z        WARN    fileset/modules.go:388  X-Pack Machine Learning is not enabled
Loaded machine learning job configurations
```
Now you can start and enable Filebeat:
```
sudo systemctl start filebeat
sudo systemctl enable filebeat
```