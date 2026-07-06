# Week 3

## Day 1

### OpenBao

- Shamir's secret sharing
  - Divides sensititve pieces of data into multiple unique parts (shares), and a quorum of shares (threshold) is required to reconstruct the sensitive data
  - `bao operator init -key-shares=<number> -key-threshold=<quorum of shares required>`
  - to unseal `bao operator unseal <key-1>` up to the number of keys required for quorum
  - Root key token can unlock without a quorum
  - You can also use a quorum of keys to regenerate a new root key token
