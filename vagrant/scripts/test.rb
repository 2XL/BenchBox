nodes = [{ :hostname => 'master', :ip => '192.168.0.40', :box => "", :box_url => false},
#         { :hostname => 'agent1', :ip => '192.168.0.41', :box => box },
#   { :hostname => 'slave42', :ip => '192.168.0.42', :box => box },
#   { :hostname => 'slave43', :ip => '192.168.0.43', :box => 'precise32' },
#   { :hostname => 'slave44', :ip => '192.168.0.44', :box => 'precise32' },
#   { :hostname => 'slave45', :ip => '192.168.0.45', :box => 'precise32' },
#   { :hostname => 'slave46', :ip => '192.168.0.46', :box => 'precise32' },
#   { :hostname => 'slave47', :ip => '192.168.0.47', :box => 'precise32' },
#   { :hostname => 'slave48', :ip => '192.168.0.48', :box => 'precise32' },
]

puts "instance slaves"
(1..3).each do |i|
  puts i
  nodes.push({:hostname => "slave#{i}", :ip=> "192.168.0.#{i+40}", :box=> ""})
end

puts nodes