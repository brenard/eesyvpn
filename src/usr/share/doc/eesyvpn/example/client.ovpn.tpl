## EesyVPN/OpenVPN Client configuration
tls-client
client
dev tap

proto tcp

# Try to preserve some state across restarts.
persist-key
persist-tun
resolv-retry infinite

remote %%HOSTNAME%% %%VPN_PORT%%

key %%KEY%%
cert %%CERT%%
ca ca.crt

remote-cert-tls server
auth-nocache

# Hardening
cipher AES-256-CBC
auth SHA512

key-direction 1
tls-auth ta.key

compress lz4
verb 3

# Required on Microsoft Windows 7
route-method exe
route-delay 2
