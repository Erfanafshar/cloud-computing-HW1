# VirtualBox API Server

This system implements a RESTful API for managing VirtualBox virtual machines. The API is designed to be used for remote lifecycle control and resource management of virtual machines. All commands are issued via HTTP in JSON format and require authentication via tokens.

## Implemented Features

- **VM Lifecycle Control**  
  - Start and stop a VM (`powering on`, `powering off`)  
  - Check the status of a specific VM  
  - Retrieve status of all VMs

- **VM Creation and Cloning**  
  - Create a new VM (from scratch or by cloning an existing one)  
  - Delete an existing VM

- **VM Configuration**  
  - Change CPU and RAM allocation for a VM

- **VM File Operations**  
  - Upload a file to a VM  
  - Transfer a file from one VM to another

- **Command Execution**  
  - Execute shell commands on a specified VM and return the output

- **Authentication and Access Control**  
  - Token-based user login and session control  
  - Users must obtain a token to perform any API action  
  - Admin user has full access; non-admin users have limited command permissions

- **HTTP Interface and Request Format**  
  - All API requests follow standard JSON format  
  - Sample command:
    ```json
    {
      "command": "status",
      "vmName": "VM1"
    }
    ```

- **Output Format**  
  - JSON responses include execution status, VM details, or command output

- **Multitenancy Support**  
  - Logical separation of user access via token-based control and scoped commands

## Notes

- The API server was tested using Postman  
- All functionality was demonstrated using VirtualBox running Ubuntu Server VMs  
- Networking was configured to allow SSH and inter-VM communication  
- File paths and operations are assumed to be within the `/home/` directory of each VM
