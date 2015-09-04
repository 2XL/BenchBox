class owncloud (
  $confdir                 = $::owncloud::params::confdir,
  $package_name            = $::owncloud::params::package_name,
  $service_name            = $::owncloud::params::service_name,
  $template                = 'owncloud/config.xml.orig.erb',
  $stacksync               = 'owncloud/owncloud.erb',
# vsftpd.conf options
  $username                 = 'someusername',
  $queuename                = '',
  $machinename              = 'somehostname',
  $autostart                = 'true',
  $notifications            = 'true',
  $apilogurl                = 'http://localhost/ownc/apiput',
  $language                   = 'es_ES',
  $remotelogs               = '',
  $rmq_host                 = '10.30.236.140',
  $rmq_port                = '5672',

)inherits ::owncloud::params {
  host {
    'owncserver':
      ip => $rmq_host
  #    ip => '10.30.233.0'
  # dhcp :: mac( 08:00:27:1e:89:5e )
  }


  case $::operatingsystem {
  # centos,fedora,rhel,redhat: {}
    debian,ubuntu: {
      class { 'owncloud::package::debian': }
    }
    default: {
      fail("Module ${module_name} is not supported on ${::operatingsystem}")
    }
  }

# descargar deb7 :: bin directament :: http://download.opensuse.org/repositories/isv:/ownCloud:/desktop/Debian_7.0/amd64/owncloud-client_1.8.4-1_amd64.deb
#
#  package { 'owncloud':
#    ensure => present,
#  }



# generar els instalar owncloud
#

}