# vim module #

[![Build Status](
https://api.travis-ci.org/ghoneycutt/puppet-module-vim.png?branch=master)](https://travis-ci.org/ghoneycutt/puppet-module-vim)

This module manages vim and root's .vimrc file and .vim directory.

===

# Compatibility #

Puppet v3 (optionally with future parser) and v4 with Ruby versions 1.8.7, 1.9.3, 2.0.0 and 2.1.0.

## OS Distributions ##

This module has been tested to work on the following systems.

* Debian 6
* EL 5
* EL 6
* EL 7
* Suse 10
* Suse 11
* Suse 12
* Solaris 10
* Solaris 11
* Ubuntu 12.04
* Ubuntu 14.04

===

# Parameters #

package_provider
----------------
String to define the package provider to use.

- *Default*: undef

package_list
------------
String or Array of the related vim packages. 'USE_DEFAULTS' will choose packages based on the osfamily.

- *Default*: USE_DEFAULTS

root_vimrc_source
-----------------
Path to .vimrc on master in the form of [module]/[filename]

- *Default*: vim/vimrc

root_vimrc_path
---------------
Where to install the root .vimrc file.

- *Default*: ${::root_home}/.vimrc

root_vimrc_owner
----------------
The .vimrc owner.

- *Default*: root

root_vimrc_group
----------------
The .vimrc group.

- *Default*: root

root_vimrc_mode
---------------
The .vimrc mode.

- *Default*: 0644

root_vim_dir_source
-------------------
Path to .vim/ on master in the form of [module]/[filename]

- *Default*: vim/vim

root_vim_dir_path
-----------------
Where to install the root .vim directory.

- *Default*: ${::root_home}/.vim

root_vim_dir_owner
------------------
The .vim directory owner.

- *Default*: root

root_vim_dir_mode
-----------------
The .vim directory mode.

- *Default*: 0644
