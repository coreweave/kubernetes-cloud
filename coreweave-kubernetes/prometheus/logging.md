# Logging

CoreWeave uses Grafana Loki for log aggregation. We are able to forward your namespace’s logs directly to your own Loki instance or to any of the following targets by simply providing credentials and target information. Direct access to CoreWeave logs, without exporting to your own log collector is currently not supported. Deploying loki in your namespace is straightforward, and the logs stored in there can be explored using Grafana deployed via [CoreWeave Apps](https://apps.coreweave.com).\


### Supported Log Export Targets

| Target                                      | Description                                                                  |
| ------------------------------------------- | ---------------------------------------------------------------------------- |
| <p> </p><p>boundary</p><p> </p>             | Sends annotations to Boundary based on Logstash events                       |
| <p> </p><p>circonus</p><p> </p>             | Sends annotations to Circonus based on Logstash events                       |
| <p> </p><p>cloudwatch</p><p> </p>           | Aggregates and sends metric data to AWS CloudWatch                           |
| <p> </p><p>datadog</p><p> </p>              | Sends events to DataDogHQ based on Logstash events                           |
| <p> </p><p>datadog_metrics</p><p> </p>      | Sends metrics to DataDogHQ based on Logstash events                          |
| <p> </p><p>dynatrace</p><p> </p>            | Sends events to Dynatrace based on Logstash events                           |
| <p> </p><p>elasticsearch</p><p> </p>        | Stores logs in Elasticsearch                                                 |
| <p> </p><p>ganglia</p><p> </p>              | Writes metrics to Ganglia’s gmond                                            |
| <p> </p><p>gelf</p><p> </p>                 | Generates GELF formatted output for Graylog2                                 |
| <p> </p><p>google_bigquery</p><p> </p>      | Writes events to Google BigQuery                                             |
| <p> </p><p>google_cloud_storage</p><p> </p> | Uploads log events to Google Cloud Storage                                   |
| <p> </p><p>google_pubsub</p><p> </p>        | Uploads log events to Google Cloud Pubsub                                    |
| <p> </p><p>graphite</p><p> </p>             | Writes metrics to Graphite                                                   |
| <p> </p><p>graphtastic</p><p> </p>          | Sends metric data on Windows                                                 |
| <p> </p><p>http</p><p> </p>                 | Sends events to a generic HTTP or HTTPS endpoint                             |
| <p> </p><p>influxdb</p><p> </p>             | Writes metrics to InfluxDB                                                   |
| <p> </p><p>irc</p><p> </p>                  | Writes events to IRC                                                         |
| <p> </p><p>juggernaut</p><p> </p>           | Pushes messages to the Juggernaut websockets server                          |
| <p> </p><p>kafka</p><p> </p>                | Writes events to a Kafka topic                                               |
| <p> </p><p>librato</p><p> </p>              | Sends metrics, annotations, and alerts to Librato based on Logstash events   |
| <p> </p><p>loggly</p><p> </p>               | Ships logs to Loggly                                                         |
| <p> </p><p>lumberjack</p><p> </p>           | Sends events using the lumberjack protocol                                   |
| <p> </p><p>metriccatcher</p><p> </p>        | Writes metrics to MetricCatcher                                              |
| <p> </p><p>mongodb</p><p> </p>              | Writes events to MongoDB                                                     |
| <p> </p><p>nagios</p><p> </p>               | Sends passive check results to Nagios                                        |
| <p> </p><p>nagios_nsca</p><p> </p>          | Sends passive check results to Nagios using the NSCA protocol                |
| <p> </p><p>opentsdb</p><p> </p>             | Writes metrics to OpenTSDB                                                   |
| <p> </p><p>pagerduty</p><p> </p>            | Sends notifications based on preconfigured services and escalation policies  |
| <p> </p><p>pipe</p><p> </p>                 | Pipes events to another program’s standard input                             |
| <p> </p><p>rabbitmq</p><p> </p>             | Pushes events to a RabbitMQ exchange                                         |
| <p> </p><p>redis</p><p> </p>                | Sends events to a Redis queue using the RPUSH command                        |
| <p> </p><p>redmine</p><p> </p>              | Creates tickets using the Redmine API                                        |
| <p> </p><p>riak</p><p> </p>                 | Writes events to the Riak distributed key/value store                        |
| <p> </p><p>riemann</p><p> </p>              | Sends metrics to Riemann                                                     |
| <p> </p><p>s3</p><p> </p>                   | Sends Logstash events to the Amazon Simple Storage Service                   |
| <p> </p><p>sns</p><p> </p>                  | Sends events to Amazon’s Simple Notification Service                         |
| <p> </p><p>solr_http</p><p> </p>            | Stores and indexes logs in Solr                                              |
| <p> </p><p>sqs</p><p> </p>                  | Pushes events to an Amazon Web Services Simple Queue Service queue           |
| <p> </p><p>statsd</p><p> </p>               | Sends metrics using the statsd network daemon                                |
| <p> </p><p>stomp</p><p> </p>                | Writes events using the STOMP protocol                                       |
| <p> </p><p>syslog</p><p> </p>               | Sends events to a syslog server                                              |
| <p> </p><p>tcp</p><p> </p>                  | Writes events over a TCP socket                                              |
| <p> </p><p>timber</p><p> </p>               | Sends events to the Timber.io logging service                                |
| <p> </p><p>udp</p><p> </p>                  | Sends events over UDP                                                        |
| <p> </p><p>webhdfs</p><p> </p>              | Sends Logstash events to HDFS using the webhdfs REST API                     |
| <p> </p><p>websocket</p><p> </p>            | Publishes messages to a websocket                                            |
| <p> </p><p>workplace_search</p><p> </p>     | <p> </p><p>Sends events to the Elastic Workplace Search solution</p><p> </p> |
| <p> </p><p>xmpp</p><p> </p>                 | Posts events over XMPP                                                       |
| <p> </p><p>zabbix</p><p> </p>               | Sends events to a Zabbix server                                              |

To set up log forwarding, contact support at support@coreweave.com.
