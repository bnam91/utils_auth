# utils_auth

Google OAuth2 인증 유틸리티 (JavaScript/Node.js 및 Python 지원)

## 버전

현재 버전: **1.0.0**

버전 정보는 다음 파일에서 확인할 수 있습니다:
- `package.json` (Node.js)
- `VERSION` (일반 텍스트)

## 기능

- Google OAuth2 인증 (JavaScript/Node.js 및 Python)
- 자동 토큰 갱신
- Google Sheets, Drive, Docs, Calendar, Forms API 지원
- 환경 변수 기반 설정 (.env 파일)
- JavaScript와 Python 간 토큰 파일 호환성

## 설치

### 직접 사용

```bash
git clone https://github.com/bnam91/utils_auth.git
cd utils_auth
npm install
```

### 서브모듈로 사용

```bash
# 다른 프로젝트에 서브모듈로 추가
git submodule add https://github.com/bnam91/utils_auth.git utils_auth

# 또는 npm 패키지로 설치 (추후 npm publish 예정)
npm install utils-auth
```

서브모듈로 사용할 때는 환경 변수 설정 방법:
1. 환경 변수 `UTILS_AUTH_ENV_PATH`로 .env 파일 경로 지정
2. 또는 현재 작업 디렉토리에 `.env` 파일 배치
3. 또는 시스템 환경 변수로 `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` 설정

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

#### 직접 사용
```javascript
const auth = require('./auth.js');

async function main() {
  const creds = await auth.getCredentials();
  // API 사용
}
```

#### 서브모듈로 사용
```javascript
// 서브모듈 디렉토리에서
const auth = require('./utils_auth/auth.js');

// 또는 npm 패키지로 설치한 경우
const auth = require('utils-auth');

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

