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
  $rmq_host                 = '130.206.36.143',
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
  $p_repo_connection_authurl    = 'http://130.206.36.143:5000/v2.0/tokens',
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
  exec { 'download_stacksync_client':
    command => "wget https://github.com/stacksync/desktop/releases/download/v2.0.1/stacksync_2.0.1_all.deb",
    path    => ['/usr/bin/', '/bin/'],
    cwd     => '/home/vagrant/desktop/packaging/debian',
    onlyif  => '[ ! -e "/usr/bin/stacksync" ]'
  }


  ->
  exec {
    'doing_foo_dpkg':
      command => 'sudo dpkg -i stacksync_2.0.1_all.deb',
      path    => ['/usr/bin/', '/bin/'],
      cwd     => '/home/vagrant/desktop/packaging/debian',
      onlyif  => '[ ! -e "/usr/bin/stacksync" ]'
  }->
  file {
    ['/usr/bin/stacksync']:
      recurse => true,
      ensure  => file,
      mode    => 0755,
      content => template($stacksync),
  }

  host {
    'syncserver':
      ip => $rmq_host
  # dhcp :: mac( 08:00:27:1e:89:5e )
  }



}



