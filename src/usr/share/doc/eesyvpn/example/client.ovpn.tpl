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

<key>
%%KEY%%
</key>
<cert>
%%CERT%%
</cert>
<ca>
%%CACRT%%
</ca>
remote-cert-tls server
auth-nocache

cipher AES-256-CBC

key-direction 1
<tls-auth>
%%TA_KEY%%
</tls-auth>

comp-lzo
verb 3

# Required on Microsoft Windows 7
route-method exe
route-delay 2
