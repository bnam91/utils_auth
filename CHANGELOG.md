# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-XX

### Added
- Google OAuth2 인증 모듈 (JavaScript/Node.js 및 Python 지원)
- Google Sheets API 연동 기능
- 자동 토큰 갱신 기능
- 환경 변수 기반 설정 (.env 파일 지원)
- JavaScript와 Python 간 토큰 파일 호환성

### Features
- `auth.js`: Node.js용 Google OAuth2 인증 모듈
- `auth.py`: Python용 Google OAuth2 인증 모듈
- `read_sheet_test.js`: Google Sheets 데이터 읽기 예제 (JavaScript)
- `read_sheet_test.py`: Google Sheets 데이터 읽기 예제 (Python)

### Supported APIs
- Google Drive API
- Google Sheets API
- Google Docs API
- Google Calendar API
- Google Forms API

