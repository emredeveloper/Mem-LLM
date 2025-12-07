# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.2.x   | :white_check_mark: |
| 2.1.x   | :white_check_mark: |
| 2.0.x   | :x:                |
| < 2.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. Email your findings to: **karatasqemre@gmail.com**
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Response Time**: We aim to respond within 48 hours
- **Updates**: We will keep you informed of progress
- **Credit**: We will credit reporters (unless anonymity is requested)
- **Fix Timeline**: Critical issues will be addressed within 7 days

## Security Features

Mem-LLM includes several security features:

### Prompt Injection Protection (v1.1.0+)

- Detects 15+ attack patterns
- Risk-level assessment (safe, low, medium, high, critical)
- Input sanitization
- Enable with: `enable_security=True`

### API Authentication (v2.2.8+)

- API key authentication
- Rate limiting
- Permission-based access control

### Local-First Architecture

- 100% local processing option
- No data sent to external servers
- Full data sovereignty

## Best Practices

When using Mem-LLM in production:

1. **Enable Security**: Use `enable_security=True`
2. **Change Default Keys**: Replace development API keys
3. **Use HTTPS**: Deploy API behind HTTPS proxy
4. **Limit Access**: Use API keys with minimal permissions
5. **Monitor Logs**: Review access and error logs
6. **Update Regularly**: Keep Mem-LLM updated

## Security Checklist

- [ ] Security features enabled
- [ ] Default API keys changed
- [ ] Rate limiting configured
- [ ] HTTPS enabled in production
- [ ] Database access restricted
- [ ] Logs monitored

## Known Security Considerations

1. **Local LLM Servers**: Ensure Ollama/LM Studio are not exposed to public networks
2. **Memory Storage**: SQLite files contain conversation history - secure appropriately
3. **API Endpoints**: Use authentication in production deployments

## Contact

- **Security Issues**: karatasqemre@gmail.com
- **General Questions**: GitHub Issues
- **Author**: C. Emre Karatas ([@emredeveloper](https://github.com/emredeveloper))
