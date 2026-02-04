# Contributing to SIH Globus Toolkit

Guidelines for internal contributors. 

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/sih-globus.git
   cd sih-globus
   ```

2. **Set up Python environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements-docs.txt
   ```

3. **Install pre-commit hooks** (optional):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Documentation Development

### Local Development Server

```bash
mkdocs serve
```

Navigate to `http://127.0.0.1:8000` to see live updates as you edit.

### Adding New Pages

1. Create markdown files in the `docs/` directory
2. Update `mkdocs.yml` navigation structure
3. Test locally with `mkdocs serve`
4. Build with `mkdocs build` to check for errors

## Code Contributions

### Script Development

- Follow Python best practices
- Use type hints where appropriate
- Include docstrings for functions
- Handle errors gracefully

### Testing

```bash
# Lint code
flake8 scripts/
black --check scripts/

# Test syntax
python -c "import py_compile; [py_compile.compile(f, doraise=True) for f in ['scripts/bulk_invite.py', 'scripts/group_admin.py']]"

# Run demo
./scripts/demo.py
```

## Commit Conventions

Use conventional commit prefixes:

- `feat:` - New features
- `fix:` - Bug fixes  
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Testing updates
- `chore:` - Maintenance tasks

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test thoroughly
5. Submit a pull request with clear description

## Issues and Questions

- Use GitHub Issues for bug reports and feature requests
- Include relevant error messages and environment details
- Check existing issues before creating new ones