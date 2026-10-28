# Changelog

## [3.0.0](https://github.com/dbrattli/OSlash/compare/oslash-v2.0.0...oslash-v3.0.0) (2026-10-28)


### ⚠ BREAKING CHANGES

* correct public typing contracts ([#67](https://github.com/dbrattli/OSlash/issues/67))

### Features

* add error-accumulating validation ([#68](https://github.com/dbrattli/OSlash/issues/68)) ([cec0c6b](https://github.com/dbrattli/OSlash/commit/cec0c6bcfa1be30dca627e2b031b12b7a53df149))


### Bug Fixes

* correct public typing contracts ([#67](https://github.com/dbrattli/OSlash/issues/67)) ([bae0e4d](https://github.com/dbrattli/OSlash/commit/bae0e4da0aa6182f1451b61ed3833aa9cfe4b851))
* preserve file input when mapping IO actions ([#50](https://github.com/dbrattli/OSlash/issues/50)) ([18000ca](https://github.com/dbrattli/OSlash/commit/18000ca6977fe0e4d8ab3f0a339caa502480f2d4))


### Documentation

* align Reader tutorial and API descriptions with current interfaces ([#51](https://github.com/dbrattli/OSlash/issues/51)) ([ce7a93c](https://github.com/dbrattli/OSlash/commit/ce7a93c3e934868ae5d56fb92a0e6031b568b5bf))

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
