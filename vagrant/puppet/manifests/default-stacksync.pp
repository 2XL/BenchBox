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
  }
  ->
  package {
    'python-scipy':
      ensure   => 'installed',
  }
  ->
  class {
    'benchbox':
  }

  ->
  exec {
    'launch_benchbox_simulator':
      command => 'python /home/vagrant/simulator/executor.p-o 100 -p sync -t 1 -f stacksync_folder -x StackSync &',
    # sudo kill -9 $(ps -ef | grep -i stacksync | grep -v \'grep\' | awk '{print $2}')
      user    => 'vagrant',
      group   =>'vagrant',
      path    => ['/usr/bin', '/bin/'],
      cwd     => '/home/vagrant/simulator'
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
  }->
  class { 'python' :
    version    => 'system',
    pip        => true,
    dev        => true,
    virtualenv => true
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
      rmq_host                  => '10.30.239.198',
      p_repo_connection_authurl => 'http://10.30.239.198:5000/v2.0/tokens'
  }->

  file {
    ['/home/vagrant/stacksync_folder', '/home/vagrant/.stacksync', '/home/vagrant/.stacksync/cache']:
      ensure  => directory,
      owner   => vagrant,
      group   => vagrant,
      mode    => '0644',
      recurse => true
  }->
  package {
    ['netifaces']:
      ensure   => 'installed',
      provider => pip
  }->
  package {
    ['PIL']:
      ensure   => 'installed',
      provider => pip
  }->
  package{
    ['psutil']:
      ensure   => 'installed',
      provider => pip
  }->
  /*
package{
  ['GeoIP']:
    ensure => 'installed',
    provider => pip
}
->
  */
  package{
    'python-pcapy':
      ensure    => 'installed'
  }->
  package{
    'python-bzrlib':
      ensure => 'installed'
  }->

  package{
    'scapy':
      ensure => 'installed'
  }
  ->
  package {
    ['bitarray']:
      ensure   => 'installed',
      provider => pip
  }


  ->
  package {
    ['thrift']:
      ensure   => 'installed',
      provider => pip


  }
  ->
  exec {
    'upagrade pip setup tools with include operation...':
      command => 'sudo pip install -U setuptools',
      user    => 'vagrant',
      group   => 'vagrant',
      path    => ['/usr/bin']
  }
  ->

  package {
    ['impyla']:
      ensure   => 'installed',
      provider => pip
  }

  ->
  package {
    ['libxml2-dev']:
      ensure => installed
  }
  ->
  package{
    ['libxslt1-dev']:
      ensure => installed
  }
  ->
  package{
    ['tshark']:
      ensure => installed
  }
  ->

  package {
    ['logbook','trollius', 'mock', 'pytest', 'lxml']:
      ensure   => 'installed',
      provider => pip
  }->
  package {
    ['pyshark']:
      ensure   => 'installed',
      provider => pip
  }
  ->
  package {
    ['dpkt']:
      ensure => 'installed',
      provider => pip
  }
  ->

  /*
  exec {
    'clear_previous_client':
      command => 'sudo kill -9 $(ps -ef | grep -i stacksync | grep -v \'grep\' | awk \'{print $2}\')',
    # sudo kill -9 $(ps -ef | grep -i stacksync | grep -v \'grep\' | awk '{print $2}')
      user    => 'vagrant',
      group   =>'vagrant',
      path    => ['/usr/bin', '/bin/'],
      returns => [0, 1]
  }
  ->
  */

  exec {
    "check_presence_of_previous_execution":
      command => 'kill -9 $(head -n 1 /tmp/StackSync.pid)',
      onlyif  => 'test -e /tmp/StackSync.pid',
      user    => 'vagrant',
      group   =>'vagrant',
      path    => ['/usr/bin', '/bin/'],
      returns => [0,1]
  }
  ->


  exec {
    'launch_stacksync_client':
      command => '/usr/bin/stacksync &',
    # sudo kill -9 $(ps -ef | grep -i stacksync | grep -v \'grep\' | awk '{print $2}')
      user    => 'vagrant',
      group   =>'vagrant',
      path    => ['/usr/bin', '/bin/']
  }
/*
->
  exec {
    'fix_debian keyring':
      command => 'sudo aptitude install debian-keyring debian-archive-keyring',
      user    => 'vagrant',
      group   =>'vagrant',
      path    => ['/usr/bin', '/bin/'],
  }
  */
/*
->
class { 'nodejs':
  version => 'stable',
  target_dir => '/bin' # add binary to bin
}

# installing npm packages

package{
  'torrentjs':
    provider => npm
}
*/
}


