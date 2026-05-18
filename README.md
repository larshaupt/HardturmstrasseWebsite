# Hotel Hardturmstrasse

A five-star website for Zurich's most distinguished shared flat.

## Setup on Raspberry Pi

```bash
# 1. Clone the repo
git clone https://github.com/larshaupt/HardturmstrasseWebsite.git
cd HardturmstrasseWebsite

# 2. Install Flask
pip3 install -r requirements.txt

# 3. Set your house PIN (keep this secret)
export GUESTBOOK_PIN=yourpin

# 4. Run
python3 app.py
```

The site runs on `http://<pi-ip>:5000`.

## To run on boot (systemd)

**1. Create the service file:**

```bash
sudo nano /etc/systemd/system/hotel.service
```

Paste the following — adjust the `WorkingDirectory` path if the repo is somewhere else:

```ini
[Unit]
Description=Hotel Hardturmstrasse
After=network.target

[Service]
WorkingDirectory=/home/gio/Desktop/HardturmstrasseWebsite
Environment=GUESTBOOK_PIN=yourpin
ExecStart=/home/gio/Desktop/HardturmstrasseWebsite/env/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**2. Enable and start:**

```bash
sudo systemctl enable hotel
sudo systemctl start hotel
```

The service will now start automatically on every boot.

**Useful commands:**

```bash
sudo systemctl status hotel   # check if it's running
sudo systemctl stop hotel     # stop it
sudo systemctl restart hotel  # restart after changes (e.g. git pull)
journalctl -u hotel -f        # view live logs
```

## Security notes

- All user input is HTML-escaped server-side — no XSS possible.
- Rate limit: 3 quotes per IP per 5 minutes.
- PIN is required to post quotes. **Never commit your PIN to git.**
- For HTTPS (recommended if publicly exposed), put it behind [Caddy](https://caddyserver.com/) or a [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/).
