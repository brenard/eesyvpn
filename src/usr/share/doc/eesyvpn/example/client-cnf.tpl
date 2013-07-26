## EesyVPN/OpenVPN Client configuration
tls-client
client
dev tap

proto tcp

# Try to preserve some state across restarts.
persist-key
persist-tun
resolv-retry infinite

remote %%HOSTNAME%% 1190

key %%CN%%.key
cert %%CN%%.crt
ca ca.crt
cipher AES-256-CBC

comp-lzo
verb 3

# Required on Microsoft Windows 7
route-method exe
route-delay 2
