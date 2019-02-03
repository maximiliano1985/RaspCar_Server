[Unit]
Description=BT_autopair

[Service]
Type=simple
ExecStart=/usr/local/share/bt_autopair.py
Restart=always

[Install]
WantedBy=multi-user.target
