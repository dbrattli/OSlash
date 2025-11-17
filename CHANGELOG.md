# Changelog

## [2.0.0](https://github.com/dbrattli/OSlash/compare/oslash-v1.0.0...oslash-v2.0.0) (2025-11-17)


### ⚠ BREAKING CHANGES

* This release marks OSlash as stable with modern Python 3.12+ features, PEP 695 type parameters, and strict type checking. The minimum Python version is now 3.12.

### Features

* release OSlash 1.0 stable ([#39](https://github.com/dbrattli/OSlash/issues/39)) ([c48645f](https://github.com/dbrattli/OSlash/commit/c48645f52a740880dd5b035808f83e3977fbb4b7))
* Update the project to modern Python and tooling ([#37](https://github.com/dbrattli/OSlash/issues/37)) ([0cdc34e](https://github.com/dbrattli/OSlash/commit/0cdc34ec23c9e48dadde5da3ab8c6e0213c892e0))


### Bug Fixes

* add pipe and sequencing operators to Maybe monad ([#43](https://github.com/dbrattli/OSlash/issues/43)) ([d4a8c8b](https://github.com/dbrattli/OSlash/commit/d4a8c8b7b3beffbeadceaa165594f2ed68098b2f))
* Fix repr for Right and Left ([dd395af](https://github.com/dbrattli/OSlash/commit/dd395afe33cc9587ccb13c642f6fed9050c513fb))
* Fixes for list and removing type extensions ([#42](https://github.com/dbrattli/OSlash/issues/42)) ([8aa7307](https://github.com/dbrattli/OSlash/commit/8aa7307dfde16ca8ead01edd60690c03383587e6))
* include LICENSE file in distribution ([8fa0229](https://github.com/dbrattli/OSlash/commit/8fa02298010ab5aacca6a9d99f1903900a1d0aed))


### Documentation

* update README badges and add 1.0 highlights ([4d972aa](https://github.com/dbrattli/OSlash/commit/4d972aad74b4e1bb226c58a3f04504d0c239c923))

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
