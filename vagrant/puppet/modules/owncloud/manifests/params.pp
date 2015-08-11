# Class: vsftpd::params
#
class owncloud::params {

  $package_name = 'owncloud'
  $service_name = 'owncloud'

  case $::operatingsystem {
    'RedHat',
    'CentOS',
    'Amazon': {
      $confdir = '/etc/owncloud'
    }
    'Debian': {
      $confdir = '/vagrant'
    }
    'Ubuntu': {
      $confdir = '/vagrant'
    }
    default: {
      $confdir = '/etc/owncloud'
    }
  }

}
