# Notes for lab 3/4

## SSH Hardening

1. Edit `/etc/ssh/sshd_config
   - NOTE: make sure it is `sshd_config` not `ssh_config`
   - MUST use sudo to edit
   - Add `AllowUsers student` under authentication
   - Login attempt failed
     - **TODO**: Capture screenshot of failure
     - Didn't run `sudo sshd -t` first, but re-ran it and still got denial

## Service Minimalization
