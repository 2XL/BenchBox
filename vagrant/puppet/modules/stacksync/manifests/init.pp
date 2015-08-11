# installation in debian 7



class stacksync (
  $confdir                 = $::stacksync::params::confdir,
  $package_name            = $::stacksync::params::package_name,
  $service_name            = $::stacksync::params::service_name,
  $template                = 'stacksync/config.xml.orig.erb',
  $stacksync               = 'stacksync/stacksync.erb',
# vsftpd.conf options
  $username                 = 'guerrero',
  $queuename                = '',
  $machinename              = 'pc_gguerr201302191026',
  $autostart                = 'true',
  $notifications            = 'true',
  $apilogurl                = 'http://localhost/stack/apiput',
  $language                   = 'es_ES',
  $remotelogs               = '',
  $rmq_host                 = '10.30.239.228',
  $rmq_port                = '5672',
  $rmq_enablessl            = 'false',
  $rmq_username               = 'guest',
  $rmq_password               = 'guest',
  $rmq_rpc_exchange            = '',
  $cache_size                = '1024',
  $p_name                      = 'Nuevo perfil',
  $p_repo_chunksize             = '512',
  $p_repo_connection_username   = 'tester20:tester20',
  $p_repo_connection_apikey     = 'testpass',
  $p_repo_connection_container    = 'stacksync',
  $p_repo_connection_authurl    = 'http://10.30.239.228:5000/v2.0/tokens',
  $p_repo_encryption_password   = '',
  $p_repo_encryption_cipher     = 'None',
  $p_repo_encryption_keylength     = '128',
  $p_folder_active              = 'true',
  $p_folder_remote              = 'stacksync',
  $p_folder_local               = '/home/gguerrero/stacksync_folder',




) inherits ::stacksync::params {


  vcsrepo { '/home/vagrant/desktop':
    ensure   => latest, # present
    provider => git,
    source   => 'https://github.com/stacksync/desktop.git',
    user     => 'vagrant',
    owner    => 'vagrant',
    group    => 'vagrant',
  # require  => Exec['ssh know github'] # via ssh and etc. for private repo
  }->
  exec {
    'doing_foo_compile':
      command => 'make compile',
      path    => ['/usr/bin/', '/bin/'],
      cwd     => '/home/vagrant/desktop/packaging/debian',
      onlyif  => '[ ! -e "/usr/bin/stacksync" ]'
  }->
  exec {
    'doing_foo_package':
      command => 'make package',
      path    => ['/usr/bin/', '/bin/'],
      cwd     => '/home/vagrant/desktop/packaging/debian',
      onlyif  => '[ ! -e "/usr/bin/stacksync" ]'
  }->
  exec {
    'doing_foo_dpkg':
      command => 'sudo dpkg -i stacksync_2.0.1_all.deb', # maybe use a regular expression??? failure ...
      path    => ['/usr/bin/', '/bin/'],
      cwd     => '/home/vagrant/desktop/packaging/debian'
  }->
  /*
    package { $package_name: ensure => installed }
    ->
    */
  # define a no tty startup
  file { # redefine the /usr/bin/stacksync script
    ['/usr/bin/stacksync']:
      recurse => true,
      ensure  => file,
      mode    => 0755,
      content => template($stacksync),
  /*    require => Package[$package_name] */
  }

  host {
    'syncserver':
      ip => '10.30.232.39'
  # dhcp :: mac( 08:00:27:1e:89:5e )
  }



/*
# epp(<FILE REFERENCE>, [<PARAMETER HASH>])
  file { '/etc/ntp.conf':
    ensure  => file,
    content => epp('ntp/ntp.conf.epp', {'service_name' => 'xntpd', 'iburst_enable' => true}),
  # Loads /etc/puppetlabs/code/environments/production/modules/ntp/templates/ntp.conf.epp
  }
*/
# customize each vagrant client startup user credentials for each box
/*
->
file {
  "${confdir}/config.xml":
    require => Package[$package_name],
    content => template($template),
    notify  => Service[$service_name],   # when the config file changes notify to the service
}
*/
# assurance that the service is running
/*
service { $service_name:
  require   => Package[$package_name],
  enable    => true,
  ensure    => running,
  hasstatus => true,
}
*/
}



