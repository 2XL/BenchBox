class owncloud::package::debian() {

  apt::key { 'owncloud':
    key        => 'BA684223',
    key_source => 'http://download.opensuse.org/repositories/isv:ownCloud:desktop/Debian_7.0/Release.key',
  } ->
  apt::source { 'owncloud-client':
    location    => 'http://download.opensuse.org/repositories/isv:/ownCloud:/desktop/Debian_7.0/',
    repos       => '',
    release     => '/',
    include_src => false,
    before      => Package['owncloud'],
  }->
  file {
    '/tmp/thescript':
      ensure => file,
      mode => '0775',
      source => 'puppet:///modules/owncloud/installClient.sh'
  }->
  exec {
    'install owncloud-client':
      command => '/tmp/thescript',
      path    => ['/bin','/usr/bin'],
      onlyif  => '/tmp/thescript',
      require => File['/tmp/thescript']
  }
/*
install the client and fix the key ring
todo: launch a cron with 30s delay interval
*/


}