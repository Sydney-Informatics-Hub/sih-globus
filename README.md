# SIH Globus Toolkit

Streamlined tools for Globus CLI administration, with focus on group management and bulk operations.

[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue)](https://yourusername.github.io/sih-globus/)
[![CI](https://github.com/yourusername/sih-globus/workflows/CI/badge.svg)](https://github.com/yourusername/sih-globus/actions)

## 📖 Documentation

**For complete documentation, visit: [https://yourusername.github.io/sih-globus/](https://yourusername.github.io/sih-globus/)**

The documentation includes:
- 🚀 [Quick Start Guide](https://yourusername.github.io/sih-globus/quickstart/)
- 🛠 [Administrative Tools](https://yourusername.github.io/sih-globus/tools/overview/)
- 📋 [Common Workflows](https://yourusername.github.io/sih-globus/workflows/common-tasks/)
- 🔧 [Installation Instructions](https://yourusername.github.io/sih-globus/installation/)

## ⚡ Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/yourusername/sih-globus.git
cd sih-globus
chmod +x scripts/*.py scripts/globus-admin

# 2. Login to Globus
globus login

# 3. List your groups
./scripts/globus-admin list

# 4. Bulk invite users
./scripts/globus-admin invite GROUP_ID --users-file users.txt --role member
```

## 🤝 Contributing

We welcome contributions! Please see our detailed [Contributing Guide](https://yourusername.github.io/sih-globus/contributing/) in the documentation.

### Quick Contribution Steps

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following our coding standards
4. **Test your changes**:
   ```bash
   # Test scripts
   ./scripts/demo.py
   
   # Lint code
   flake8 scripts/
   black --check scripts/
   ```
5. **Commit with conventional format**:
   ```bash
   git commit -m "feat: add new bulk operation feature"
   ```
6. **Push and create a Pull Request**

### Commit Convention

Use these prefixes for commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation updates
- `refactor:` - Code refactoring
- `test:` - Testing improvements
- `chore:` - Maintenance tasks

### Development Setup

```bash
# Setup documentation environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements-docs.txt

# Run documentation locally
mkdocs serve
```

## 📋 Features

- **Bulk Operations**: Invite multiple users to groups simultaneously
- **Group Management**: Comprehensive tools for group administration
- **University Integration**: Designed for University of Sydney workflows
- **CLI Wrapper**: Simplifies complex Globus CLI operations
- **Error Handling**: Robust error handling and reporting
- **Dry-run Mode**: Test operations before execution

## 📞 Support

- **Documentation**: [https://yourusername.github.io/sih-globus/](https://yourusername.github.io/sih-globus/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/sih-globus/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/sih-globus/discussions)

## 📜 License

This project is maintained by the Sydney Informatics Hub for the University of Sydney community.

---

*For detailed documentation, examples, and workflows, please visit our [documentation site](https://yourusername.github.io/sih-globus/).*
