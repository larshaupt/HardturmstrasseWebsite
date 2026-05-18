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

Create `/etc/systemd/system/hotel.service`:

```ini
[Unit]
Description=Hotel Hardturmstrasse
After=network.target

[Service]
WorkingDirectory=/home/pi/HardturmstrasseWebsite
Environment=GUESTBOOK_PIN=yourpin
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then: `sudo systemctl enable --now hotel`

## Security notes

- All user input is HTML-escaped server-side — no XSS possible.
- Rate limit: 3 quotes per IP per 5 minutes.
- PIN is required to post quotes. **Never commit your PIN to git.**
- For HTTPS (recommended if publicly exposed), put it behind [Caddy](https://caddyserver.com/) or a [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/).
