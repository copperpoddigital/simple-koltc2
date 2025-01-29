# Security Policy

## Supported Versions

The Simple To-Do List App currently maintains security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

Only Python versions 3.6 and above are supported for secure operation of the application.

## Reporting a Vulnerability

We take security vulnerabilities seriously. Please follow these steps to report any security issues:

1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. Submit your report through GitHub Security Advisories
3. Include detailed steps to reproduce the vulnerability
4. Provide any relevant error messages or logs
5. Suggest potential fixes if possible

You can expect:
- Initial response within 48 hours
- Regular updates on the status of your report
- Full credit in security advisories (if desired)

## Security Considerations

### File Permissions
- Task data files are created with 0600 permissions (owner read/write only)
- Application enforces strict file access controls
- Backup files maintain identical permission settings
- File operations use atomic writes to prevent corruption

### Data Storage
- All data stored locally in user's home directory
- No external network connections required
- File paths restricted to prevent directory traversal
- Maximum file size limited to 1MB for data files

### Input Validation
- Task descriptions limited to 1-200 characters
- Special characters filtered from input
- Menu selections strictly validated
- Task numbers bounds-checked against current list

## Security Configuration

The following security settings are enforced:

| Setting | Value | Purpose |
|---------|--------|---------|
| File Mode | 0600 | Restrict file access to owner only |
| Max File Size | 1MB | Prevent resource exhaustion |
| Input Timeout | None | Local-only access model |
| Backup Retention | 1 version | Minimize data exposure |
| Log Level | ERROR | Prevent information disclosure |

## Error Handling

Security-related errors are handled with the following codes:

| Code | Description | Action |
|------|-------------|---------|
| E001 | File permission denied | Check file ownership and permissions |
| E002 | Invalid file access attempt | Verify user permissions |
| E003 | Data file corruption detected | Restore from backup file |
| E004 | Input validation failure | Review input guidelines |
| E005 | File size limit exceeded | Remove unnecessary tasks |

Generic error messages are used to prevent information disclosure.

## Best Practices

1. **File System**
   - Keep task files in default location
   - Do not modify file permissions
   - Maintain regular backups

2. **Usage**
   - Run as regular user (not root/admin)
   - Do not share task files
   - Close application when not in use

3. **Input**
   - Follow character limits
   - Avoid special characters
   - Use standard ASCII text

## Security Updates

- Security patches released as minor version updates
- Critical fixes announced via GitHub Security Advisories
- Update notifications provided through repository

For non-sensitive security questions, create a GitHub issue with the "security" label.