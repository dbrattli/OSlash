# Changelog

## [1.0.0](https://github.com/dbrattli/OSlash/compare/v0.6.0...v1.0.0) (2025-11-16)

### ⚠ BREAKING CHANGES

* This release marks OSlash as stable with modern Python 3.12+ features, PEP 695 type parameters, and strict type checking. The minimum Python version is now 3.12.

### Features

* Modernized to Python 3.12+ with PEP 695 type parameters ([#37](https://github.com/dbrattli/OSlash/pull/37))
* Strict type checking with pyright
* Modern tooling (uv, ruff, pre-commit)
* Comprehensive CLAUDE.md development guide
* CI/CD workflows updated to use setup-uv@v7
* Test matrix expanded to Python 3.12, 3.13, and 3.14

### Bug Fixes

* Add pipe and sequencing operators to Maybe monad ([#43](https://github.com/dbrattli/OSlash/pull/43))
* Fixes for list and removing type extensions ([#42](https://github.com/dbrattli/OSlash/pull/42))

### Project Status

* Development Status updated to "Production/Stable"
* Project ready for 1.0 stable release with 740+ GitHub stars
