# Week 1

## Day 1

### General information

- Use webcecs for course info
- Labs -> one each week
- Background reading available on the course webpage
- Proxmox (added to bookmarks)
  - https://systemsec-01.cs.pdx.edu:8006/
  - Hostname: systemsec-01
  - Port: 8000

### Infrastructure as Code (IaC)

- Idempotency
  - Op that can be executed multiple times without changing the result beyond the initial application
- Entire infrastructure is virtualized or a bare-metal (rack-mount) server at blank slate
  - Almost all are virtualized
  - Virtual infrastructure allows for destruction of infrastructure at any point
    - Allows for scripting and auditing
      - Security auditing: we are not vulnerable
- Terraform (TF) or Tofu
  - HashiCorp Configuration Language (HCL)
  - Give TF a declarative file for a machine with specific characteristics and clone from a specific base, sends to virtual provider (ex: ProxMox)
  - Files provided on gitlab
  - TF is run on local system
    - Tooling exists on local (repo)
    - We don't do much on the server
  - TF workflow
    - Initialize
      - DL provider plugins and backend
    - Validate
      - Ensure correct HCL syntax
    - Plan
      - Dry run
    - Apply
    - Destroy
  - TF files written in HCL
    - **Get a snapshot** (see readme)
      - Reverting state -> go back if something breaks
      - Useful for vulnerability analysis
  - Resource block
    - Declarative (What)
      - Key-value pairs
    - Imperitive (how)
      - Code loops and creates constructs
    - YOUR PVE NODE (systemsec-01)
    - Need to know
      - Where is it coming from
    - **Note: At no point do we create a password**
    - This block creates the VMs
- Ansible
  - Agentless config management tool
    - Nothing running on the configured server
  - Connects through SSH
  - Organizes tasks into playbooks
    - One playbook configures all 3 hosts (for this class)
  - Inventory file
    - ProxyJump to connect to ProxMox systems
      - Will be using systemsec hostname that was assigned
  - Config file
    - Config settings
  - Roles live in roles directory
  - Idempotent
    - Pulls any drift back to known configuratin state
  - Can pull in new capabilities or shell script
    - Scripts should be short and easy to audit, and **must** be documented
      - Changes will be documented in the class repo

### Environment setup

- All ProxMox upgraded to v 9
- Gitlab repo
  - Must have valid SSH key (check for desktop computer)
  - SSH setup (linked on course website)
    - SSH key generation (uses elliptic curve)
      - `ssh-keygen -t ed25519`
        - `-C` for comment
        - `-f` provide a filepath
        - Defaults to `~/.ssh`
        - Give the key a meaningful name
    - Important files
      - Private key
      - Public Key
      - Config file
      - Known hosts
      - Authorized keys
    - User Settings -> access
    - Clone repo
      - clone with SSH -> git clone <repo info>
      - Check files
      - Push create templates file up to specific server
        - ssh-copy-id -i <path to key> user@server
      - Use config file to setup ssh info
        - Hostname: systemsec-01
        - Port: 22
        - Identities only yes
