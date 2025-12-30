# utils_auth

Google OAuth2 인증을 쉽게 사용할 수 있는 유틸리티입니다. JavaScript/Node.js와 Python을 모두 지원해요.

## 설치하기

```bash
git clone https://github.com/bnam91/utils_auth.git
cd utils_auth
npm install  # Node.js용
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv  # Python용
```

## 설정하기

`config/.env` 파일을 만들고 아래처럼 입력하세요:

```
GOOGLE_CLIENT_ID=여기에_클라이언트_ID_입력
GOOGLE_CLIENT_SECRET=여기에_클라이언트_시크릿_입력
```

Google Cloud Console에서 OAuth2 클라이언트 ID와 시크릿을 발급받아야 해요.

## 사용하기

**JavaScript/Node.js:**
```javascript
const auth = require('./auth.js');
const creds = await auth.getCredentials();
```

**Python:**
```python
import auth
creds = auth.get_credentials()
```

## 예제

`read_sheet_test.js` / `read_sheet_test.py`: Google Sheets 데이터 읽기 예제
