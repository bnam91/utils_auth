# utils_auth

Google OAuth2 인증 유틸리티 (JavaScript/Node.js 및 Python 지원)

## 버전

현재 버전: **1.0.0**

버전 정보는 다음 파일에서 확인할 수 있습니다:
- `package.json` (Node.js)
- `VERSION` (일반 텍스트)
- `__version__.py` (Python)

## 기능

- Google OAuth2 인증 (JavaScript/Node.js 및 Python)
- 자동 토큰 갱신
- Google Sheets, Drive, Docs, Calendar, Forms API 지원
- 환경 변수 기반 설정 (.env 파일)
- JavaScript와 Python 간 토큰 파일 호환성

## 설치

### Node.js

```bash
npm install
```

### Python

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
```

## 설정

1. `config/.env` 파일을 생성하고 다음 환경 변수를 설정하세요:

```
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
```

2. Google Cloud Console에서 OAuth2 클라이언트 ID와 시크릿을 생성하세요.

## 사용법

### JavaScript/Node.js

```javascript
const auth = require('./auth.js');

async function main() {
  const creds = await auth.getCredentials();
  // API 사용
}
```

### Python

```python
import auth

creds = auth.get_credentials()
# API 사용
```

## 예제

- `read_sheet_test.js`: Google Sheets 데이터 읽기 예제 (JavaScript)
- `read_sheet_test.py`: Google Sheets 데이터 읽기 예제 (Python)

## 라이선스

ISC

