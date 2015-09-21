

# create simple logger table

drop table if EXISTS  logger_pcap;

create table if not EXISTS logger_pcap (
ts string,
ip_src string,
ip_tgt string,
port_src int,
port_tgt int,
protocol int,
len int
) stored as parquet;








-- -----------------------------------
-- CPU
drop table if exists logger_cpu;
create table if not exists logger_cpu (
  ts timestamp,
  cpu_usage int,
  cpu_count int,
  logger_id bigint,
  dummy_hostname string
) stored as parquet;

-- RAM
drop table if exists logger_ram;
create table if not exists logger_ram (
  ts timestamp,
  ram_usage int,
  ram_count int,
  logger_id bigint,
  dummy_hostname string
) stored as parquet;

-- NET
drop table if exists logger_net;
create table if not exists logger_net (
  ts timestamp,
  up_size int,
  down_size int,
  logger_id bigint,
  dummy_hostname string
)stored as parquet;

-- HDD
drop table if exists logger_hdd;

create table if not exists logger_hdd (
  ts timestamp,
  data_write int,
  data_read int,
  logger_id bigint,
  dummy_hostname string
) stored as parquet;

-- ID
drop table if exists logger_id;
create table if not exists logger_id(
  logger_id bigint,
  pc_client_name string,
  pc_server_name string,
  profile string,
  test_definition string
) stored as parquet;























# create logger table with more detailed fields
# can handle comparison of cpu usage between machines


drop table if exists logger_cpu;

create table if not exists logger_cpu (
  ts timestamp,
  cpu_usage int, # 1-100 cpu usage
  cpu_count int, # number of cpu

  testid bigint # current timestamp

) stored as parquet;


# can handle comparison of ram usage between machines

drop table if exists logger_ram;

create table if not exists logger_ram (
  ts timestamp,
  ram_usage int, # in bytes of usage
  ram_count int, # total of ram

  testid bigint # current timestamp
)

# can handle comparison of network traffic usage as absolute value

drop table if exists logger_net;

create table if not exists logger_net (
  ts timestamp,
  up_size int, # in bytes
  down_size int, # in bytes

  testid bigint # current timestamp
)stored as parquet;

  # the comparison between two timestamps, can be
  # difference between usage epoch



# can monitor the hard-drive utilization

drop table if exists logger_ssd;

create table if not exists logger_ssd (
  ts timestamp,
  data_write int,
  data_read int,

  testid bigint # current timestamp
)stored as parquet;

  # it makes no sense...



# can distinguish the utilization of network traffic type
  # comparison between data and metadata










# create a table defining the test, test definition table

drop table if exists logger_id;

create table if not exists logger_id(
ts timestamp,
pc_client_name string,
pc_server_id string,
profile string, # sync|cdn|backup|regular|idle
test_id bigint, # current timestamp, absolute precision
test_definition string # # define the test, can be string serialized (object) to be parsed...
) stored as parquet;

