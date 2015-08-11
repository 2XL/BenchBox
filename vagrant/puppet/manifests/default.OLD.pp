ode master {
  package {
    ['unzip','nmap']: ensure => installed
  }

  class { '::mysql::server':
    root_password    => 'vagrant',
    override_options => { 'mysqld' => {
      'bind_address' => '0.0.0.0',
      'max_connections' => '1024'
    } # overyde my.cnf
    }
  # all ip addreess on the local machine
  }

# creating a database
  mysql::db{
    'benchbox':
      user     => 'alice',
      password => 'bob',
      host     => 'localhost',
      sql      => 'tmp/test.sql',
      require  => File['/tmp/test.sql']
  }

  file { "/tmp/test.sql":
    ensure => present,
    source => "puppet:///modules/benchbox/test.sql",
  }
# create user
  mysql_user { 'vagrant@localhost':
    ensure                   => 'present',
    max_connections_per_hour => '60',
    max_queries_per_hour     => '120',
    max_updates_per_hour     => '120',
    max_user_connections     => '10',
  }
# grant user permsion
  mysql_grant { 'vagrant@localhost/benchbox.log':
    ensure     => 'present',
    options    => ['GRANT'],
    privileges => ['ALL'],
    table      => 'benchbox.log',
    user       => 'vagrant@localhost',
  }



}



node /^slave\d+/ {
  package {
    'nmap':
      ensure => installed
  }
  class { 'apt':
    update => {
      frequency => 'daily',
    },
  }->
  class {
    'git':

  }->
  class {
    'vim':
  }->
  class { 'python' :
    version    => 'system',
    pip        => true,
    dev        => true,
    virtualenv => true,
    gunicorn   => true,
  }-> package {
    ['numpy']:
      ensure   => 'installed',
      provider => pip

  }->
  package {
    ['simpy']:
      ensure => '2.3',
      provider => pip
  }->
  class {
    'benchbox':
  }

  class{
    '::mysql::client': # client to the server...

  }
}


