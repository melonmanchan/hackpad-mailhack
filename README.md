# What is this?

It's a hacked script to use Hackpad without an SMTP server, instead using sendgrid, when Hackpad is running inside
a Docker container. If this description doesn't fill your extremely specific needs, you should probably move along
;)

# Configuration

Add your SendGrid API key, name of the running docker container and the URL of your Hackpad container to config.json

# Gotchas

Docker relies a lot on sudo, so you should probably run this script with sudo, too!

