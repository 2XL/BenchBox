# this puppet deploys a client with all the software dependencies - only owncloud

# -------------------------------------------------------------------------------------------------------
# benchBox
# -------------------------------------------------------------------------------------------------------
node 'benchBox' {
  class { 'apt':
    update => {
      frequency => 'daily',
    },
  }->
  class {
    'git':
  }->
  class { 'python' :
    version    => 'system',
    pip        => true,
    dev        => true,
    virtualenv => true
  }->
  package {
    ['numpy']:
      ensure   => 'installed',
      provider => pip
  }->
  package {
    ['simpy']:
      ensure   => '2.3',
      provider => pip
  }->
  package {
    ['scipy']:
      ensure   => '0.12.0',
      provider => pip
  }->
  class {
    'benchbox':
  }
}

define download_file(
  $site="",
  $cwd="",
  $creates="") {

  exec { $name:
    path    => ['/bin','/usr/bin'],
    command => "wget ${site}/${name}",
    cwd     => $cwd,
    creates => "${cwd}/${name}", # if this files does not exist then the it ill not execute...
  }

}

# -------------------------------------------------------------------------------------------------------
# sandBox
# -------------------------------------------------------------------------------------------------------
node 'sandBox' {
  class { 'apt':
    update => {
      frequency => 'daily',
    },
  }->
  class {
    'git':
  }
  ->
  class {
    'vsftpd':
      write_enable            => 'YES',
      ftpd_banner             => 'SandBox FTP Server',
    #  chroot_local_user       => 'YES',
    #  chroot_list_enable      => 'YES',
      anonymous_enable        => 'YES',
      anon_upload_enable      => 'YES',
      anon_mkdir_write_enable => 'YES',
      pasv_min_port           => 10090,
      pasv_max_port           => 10100,
  }->
  file { ["/etc/vsftpd.user_list" ]:
      recurse => true,
      ensure  => present,
      mode    => 0777,
      content => 'vagrant vagrant',
  # ftp OOP 500 error becuase this file not present -> vsftpd
  }-> # give anonymous user ftp permision
  file { "/srv/ftp":
    ensure => "directory",
    owner  => "ftp",
    group  => "ftp",
    mode   => 755,
  }
  ->
  class{
    "owncloud":
      rmq_host => '192.168.1.240'
  }
  ->
  file {
    ['/home/vagrant/owncloud_folder']:
      ensure  => directory,
      owner   => vagrant,
      group   => vagrant,
      mode    => '0644',
      recurse => true
  }
  ->
  exec {
    'launch_stacksync_client':
      command => 'sudo kill -9 $(ps -ef | grep -i owncloudsync.sh | grep -v \'grep\' | awk \'{print $2}\');
      /vagrant/owncloudsync.sh &',
      cwd     => '/vagrant',
      user    => 'vagrant',
      group   =>'vagrant',
      path    => ['/usr/bin', '/bin/'],
  }

}

