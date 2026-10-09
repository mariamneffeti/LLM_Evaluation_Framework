# Changelog

All notable changes to this project are documented in this file.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-10-09

### Added

- FastAPI endpoints for health checks, model discovery, benchmark execution,
  run retrieval, listing, and comparison.
- A React dashboard for starting and reviewing benchmark runs.
- Provider adapters for Groq, GitHub Models, Google Gemini, and Ollama.
- JSONL benchmark loading, answer scoring, token reporting, and SQLite
  persistence.
- Docker Compose setup and GitHub Actions workflows.
- Pytest coverage for API endpoints and evaluation behavior using a mocked
  provider.
- MIT license.

### Changed

- Rewrote the README with setup instructions, architecture, API documentation,
  configuration, and project roadmap.

### Security

- Removed the committed evaluation archive and added archive and model artifact
  ignore rules.
- Confirmed `.env` is not tracked and provided `.env.example` placeholders for
  local configuration.
