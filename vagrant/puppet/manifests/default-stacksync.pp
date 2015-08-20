# this puppet deploys a client with all the software dependencies - only stacksync

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
    'java':
      distribution => 'jdk',
  }->
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
  file
  {
    ["/etc/vsftpd.user_list" ]:
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

  /*
  ->
  class { "maven::maven":
    version => "3.2.5", # version to install
  # you can get Maven tarball from a Maven repository instead than from Apache servers, optionally with a user/password
    repo    => {
    #url => "http://repo.maven.apache.org/maven2",
    #username => "",
    #password => "",
    }
  } ->
  # Setup a .mavenrc file for the specified user
  maven::environment { 'maven-env' :
    user                 => 'root',
  # anything to add to MAVEN_OPTS in ~/.mavenrc
    maven_opts           => '-Xmx1384m',       # anything to add to MAVEN_OPTS in ~/.mavenrc
    maven_path_additions => "",      # anything to add to the PATH in ~/.mavenrc
  }
  */

  ->
  class {
    "stacksync":
      rmq_host                  => '192.168.1.237',
      p_repo_connection_authurl => 'http://192.168.1.237:5000/v2.0/tokens'
  }->

  file {
    ['/home/vagrant/stacksync_folder', '/home/vagrant/.stacksync', '/home/vagrant/.stacksync/cache']:
      ensure  => directory,
      owner   => vagrant,
      group   => vagrant,
      mode    => '0644',
      recurse => true
  }
  ->
  exec {
    'clear_previous_client':
      command => 'sudo kill -9 $(ps -ef | grep -i stacksync | grep -v \'grep\' | awk \'{print $2}\');',
    # sudo kill -9 $(ps -ef | grep -i stacksync | grep -v \'grep\' | awk '{print $2}')
      user    => 'vagrant',
      group   =>'vagrant',
      path    => ['/usr/bin', '/bin/'],
  }
  ->
  exec {
    'launch_stacksync_client':
      command => 'stacksync &',
    # sudo kill -9 $(ps -ef | grep -i stacksync | grep -v \'grep\' | awk '{print $2}')
      user    => 'vagrant',
      group   =>'vagrant',
      path    => ['/usr/bin', '/bin/'],
  }
}


