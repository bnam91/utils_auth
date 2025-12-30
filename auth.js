// V1.0.0 자동갱신 (Node.js)

const fs = require("fs");
const path = require("path");
const os = require("os");
const http = require("http");
const { URL } = require("url");
const { google } = require("googleapis");
const open = require("open");
const dotenv = require("dotenv");

// .env 파일 로드 (config/.env 경로에서)
const envPath = path.join(__dirname, "config", ".env");
dotenv.config({ path: envPath });

// Google API 접근 범위 설정 (필요한 최소한의 범위만 포함)
const SCOPES = [
  "https://www.googleapis.com/auth/drive",
  "https://www.googleapis.com/auth/spreadsheets",
  "https://www.googleapis.com/auth/documents",
  "https://www.googleapis.com/auth/calendar",
  "https://www.googleapis.com/auth/forms",
];

// 환경 변수에서 클라이언트 정보 가져오기
const CLIENT_ID = process.env.GOOGLE_CLIENT_ID;
const CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET;

function getTokenPath() {
  // 운영 체제에 따른 토큰 저장 경로 반환
  if (process.platform === "win32") {
    return path.join(process.env.APPDATA || "", "GoogleAPI", "token.json");
  }
  return path.join(os.homedir(), ".config", "GoogleAPI", "token.json");
}

function ensureTokenDir() {
  // 토큰 저장 디렉토리가 없으면 생성
  const tokenDir = path.dirname(getTokenPath());
  if (!fs.existsSync(tokenDir)) {
    fs.mkdirSync(tokenDir, { recursive: true });
  }
}

function readSavedCredentials() {
  const tokenPath = getTokenPath();
  if (fs.existsSync(tokenPath)) {
    try {
      const content = fs.readFileSync(tokenPath, "utf-8");
      const json = JSON.parse(content);
      return json;
    } catch {
      return null;
    }
  }
  return null;
}

function saveCredentials(credentials) {
  ensureTokenDir();
  const tokenPath = getTokenPath();
  fs.writeFileSync(tokenPath, JSON.stringify(credentials));
}

async function getNewCredentialsViaLocalServer(oAuth2Client) {
  return new Promise((resolve, reject) => {
    const server = http.createServer(async (req, res) => {
      try {
        const reqUrl = new URL(req.url, `http://localhost`);
        if (reqUrl.pathname !== "/oauth2callback") {
          res.writeHead(404);
          res.end("Not Found");
          return;
        }

        const code = reqUrl.searchParams.get("code");
        if (!code) {
          res.writeHead(400);
          res.end("Missing code");
          return;
        }

        const { tokens } = await oAuth2Client.getToken(code);
        oAuth2Client.setCredentials(tokens);
        saveCredentials(tokens);

        res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
        res.end("인증이 완료되었습니다. 이 창을 닫으셔도 됩니다.");

        setImmediate(() => server.close());
        resolve(oAuth2Client);
      } catch (err) {
        setImmediate(() => server.close());
        reject(err);
      }
    });

    server.listen(0, async () => {
      const { port } = server.address();
      const redirectUri = `http://localhost:${port}/oauth2callback`;
      const client = new google.auth.OAuth2(CLIENT_ID, CLIENT_SECRET, redirectUri);

      // 기존 인스턴스의 리다이렉트를 로컬 서버로 교체
      oAuth2Client.redirectUri = redirectUri;

      const authUrl = client.generateAuthUrl({
        access_type: "offline",
        scope: SCOPES,
        include_granted_scopes: true,
        prompt: "consent",
      });

      try {
        await open(authUrl);
      } catch {
        // open 실패 시 URL만 콘솔에 출력
        // eslint-disable-next-line no-console
        console.log("브라우저를 열 수 없습니다. 다음 URL을 복사해 접속하세요:\n", authUrl);
      }
    });
  });
}

async function getCredentials() {
  if (!CLIENT_ID || !CLIENT_SECRET) {
    throw new Error("환경 변수 GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET 가 필요합니다.");
  }

  ensureTokenDir();
  const saved = readSavedCredentials();
  const oAuth2Client = new google.auth.OAuth2(CLIENT_ID, CLIENT_SECRET, "http://localhost");

  if (saved) {
    oAuth2Client.setCredentials(saved);
    
    // refresh_token이 있으면 항상 갱신 시도 (만료 여부와 관계없이)
    if (saved.refresh_token) {
      try {
        const { credentials } = await oAuth2Client.refreshAccessToken();
        oAuth2Client.setCredentials(credentials);
        saveCredentials(credentials);
        return oAuth2Client;
      } catch (err) {
        // 갱신 실패 시 (refresh_token이 만료되었거나 취소된 경우) 새로 인증
        console.log("토큰 갱신 실패. 재인증이 필요합니다...");
        const client = await getNewCredentialsViaLocalServer(oAuth2Client);
        return client;
      }
    }
    
    // refresh_token이 없고 토큰이 만료된 경우 새로 인증
    const isExpired = saved.expiry_date && saved.expiry_date <= Date.now();
    if (isExpired) {
      console.log("토큰이 만료되었습니다. 재인증이 필요합니다...");
      const client = await getNewCredentialsViaLocalServer(oAuth2Client);
      return client;
    }
    
    return oAuth2Client;
  }

  // 토큰이 없으면 로컬 서버를 띄워 인증 진행
  const client = await getNewCredentialsViaLocalServer(oAuth2Client);
  return client;
}

module.exports = {
  SCOPES,
  getCredentials,
  getTokenPath,
};


