# Class: vsftpd::params
#
class stacksync::params {

  $package_name = 'stacksync'
  $service_name = 'stacksync'

  case $::operatingsystem {
    'RedHat',
    'CentOS',
    'Amazon': {
      $confdir = '/etc/stacksync'
    }
    'Debian': {
      $confdir = '/vagrant'
    }
    'Ubuntu': {
      $confdir = '/vagrant'
    }
    default: {
      $confdir = '/etc/stacksync'
    }
  }

}
