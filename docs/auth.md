# Authentication

## Login Process

The Globus CLI uses OAuth2 for authentication with your institutional identity provider.

### Initial Login

```bash
globus login
```

This command will:

1. **Open your browser** to the Globus authentication page
2. **Redirect to your institution** (University of Sydney)  
3. **Authenticate via Okta** using your credentials
4. **Grant permissions** to the CLI application
5. **Store tokens locally** for future use

### University of Sydney Integration

The authentication flow is specifically configured for:

- **Identity Provider**: University of Sydney
- **Authentication Method**: Okta SSO
- **Username Format**: `username@sydney.edu.au`

## Session Management

### Check Current Session

```bash
globus session show
```

Example output:
```
Username: gsam0138@sydney.edu.au
Session expires: 2026-01-27 14:30:00 UTC
Scopes: openid profile email urn:globus:auth:scope:transfer.api.globus.org:all
```

### Check Identity

```bash
globus whoami
```

Shows your primary identity and any linked accounts.

### Session Refresh

Sessions automatically refresh when needed, but you can manually refresh:

```bash
globus session update
```

## Multiple Identities

If you have multiple Globus identities (institutional + personal accounts):

### List All Identities

```bash
globus get-identities --provision-identity username@domain.com
```

### Switch Primary Identity

```bash
globus session update --identity username@otherdomain.edu
```

## Logout

### Logout from Current Session

```bash
globus logout
```

### Logout from All Sessions

```bash
globus logout --all
```

## Troubleshooting Authentication

### Browser Issues

If the browser doesn't open automatically:

1. Copy the URL from the terminal
2. Paste into your browser
3. Complete authentication
4. Copy the authorization code back to terminal

### Token Expiration

If you get authentication errors:

```bash
# Check session status
globus session show

# Refresh if expired
globus session update

# Or re-login if needed
globus logout
globus login
```

### Institution Not Recognized

If University of Sydney authentication fails:

1. Verify you're using the correct login portal
2. Check with IT support for Globus access
3. Ensure your account has necessary permissions

### Proxy/Firewall Issues

If behind institutional firewall:

1. Configure proxy settings:
   ```bash
   export HTTP_PROXY=http://proxy.sydney.edu.au:8080
   export HTTPS_PROXY=http://proxy.sydney.edu.au:8080
   ```

2. Contact IT support for firewall exceptions

## Security Best Practices

!!! warning "Token Security"
    - Tokens are stored in `~/.globus/`
    - Don't share or copy these files
    - Use `globus logout` on shared computers
    - Regularly refresh sessions

### Token Storage Location

Tokens are stored in:
```
~/.globus/
├── config.yml
├── tokens.json
└── client-info.json
```

### Permissions and Scopes

The CLI requests these scopes:
- **OpenID**: Basic identity information
- **Profile**: Name and email
- **Transfer API**: File transfer operations
- **Groups API**: Group management (if available)

---

Next: [Administrative Tools Overview](tools/overview.md)