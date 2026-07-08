# Week 3

## Day 1

### OpenBao

- Shamir's secret sharing
  - Divides sensititve pieces of data into multiple unique parts (shares), and a quorum of shares (threshold) is required to reconstruct the sensitive data
  - `bao operator init -key-shares=<number> -key-threshold=<quorum of shares required>`
  - to unseal `bao operator unseal <key-1>` up to the number of keys required for quorum
  - Root key token can unlock without a quorum
  - You can also use a quorum of keys to regenerate a new root key token

## Day 2

### Docker

- Docker daemon
  - Orchestration layer for managing containers
- CLI
  - Programmatically control the orchestrator
- Docker Hub
  - public image registry (similar to github)
- Image
  - File system
  - `docker pull`
    - Pulls an image from docker hub
    - `docker pull <name_of_image>:<version_of_image>`
  - `docker image prune`
    - remove unused images
- Container
  - Running instance of an image (see course website)
  - Architecture is important when running containers
- Proxmox `create CT`
  - Creates a container
  - There is no ability to customize an image on proxmox

### Running Docker containers

- Calling `docker run` gives you a new container instance from a specified image
- Multiple commands must be changed with conditional running
  - State reverts after each command
- Every time you invoke `run` you add a new layer to the file system
  - These layers are cached
    - Can ignore with `docker build --no-cache`
