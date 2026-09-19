# assuredmro.com — static site

Assured MRO (a dba of Huntington Hospitalist Group Inc) — nationwide Medical Review Officer services.

Plain static HTML in `site/` served by nginx behind Traefik on the VPS (31.97.135.220), same setup as hhghealth.org.

- `site/index.html` — home
- `site/pricing/index.html` — plans + cost estimator (Square checkout links, Jotform quote prefill)
- `site/welcome/index.html` — post-checkout page (Square redirects here)
- `site/_conf/default.conf` — nginx config
- Quote form: https://form.jotform.com/262617390750055

## Deploy
On the VPS: `cd /root/assuredmro-src && ./deploy.sh` (auto-runs from the autodeploy cron once registered).

## DNS
A @ 31.97.135.220 · A www 31.97.135.220
