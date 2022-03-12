# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2022-??-??
### Added
### Changed
### Removed
## [1.0.0] - 2022-03-12
### Added
- Added PostgreSQL support for Heroku deployments (@the-mann)
- Added Github Actions (@bmselewski, @the-mann)
- Store Google Login environment variables in Heroku (@bmselewski, @the-mann)
- Populate Google Login credentials based on environment variables `CLIENT_ID` and `SECRET_KEY`
- Tutorial in `README.md` for developers to spin up a development environment (@the-mann, @bmselewski)
- Multi stage Heroku deployments (@the-mann, @bmselewski)

### Changed
- Fixed `Procfile` issues, where it would refer to the unrefactored name of the Django project rather than `word_of_mouth`

### Removed
- Nothing


[Unreleased]: https://github.com/uva-cs3240-s22/group-project-a-07/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/uva-cs3240-s22/group-project-a-07/releases/tag/v1.0.0