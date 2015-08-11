
/*
service { 'benchbox':
  ensure     => running,
  enable     => true,
  hasstatus  => true,
  hasrestart => true,
  require    => Package['nginx'],
  subscribe  => File['/etc/nginx/nginx.conf'],
}
*/

service { 'stacksync':
  ensure => 'running',
  enable => true,
}