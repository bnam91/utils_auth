# V1.0.0 자동갱신

import os
import sys
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

# 환경 변수 로드 (config/.env 경로에서)
env_path = os.path.join(os.path.dirname(__file__), "config", ".env")
load_dotenv(env_path)

# Google API 접근 범위 설정 (필요한 최소한의 범위만 포함)
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/forms'
]

# 환경 변수에서 클라이언트 정보 가져오기
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

def get_token_path():
    """운영 체제에 따른 토큰 저장 경로 반환"""
    if sys.platform == "win32":
        return os.path.join(os.environ["APPDATA"], "GoogleAPI", "token.json")
    return os.path.join(os.path.expanduser("~"), ".config", "GoogleAPI", "token.json")

def ensure_token_dir():
    """토큰 저장 디렉토리가 없으면 생성"""
    token_dir = os.path.dirname(get_token_path())
    if not os.path.exists(token_dir):
        os.makedirs(token_dir)

def check_token_status():
    """토큰 상태를 확인하고 상태 메시지를 반환"""
    token_path = get_token_path()
    
    if not os.path.exists(token_path):
        return {
            'status': 'no_token',
            'message': '저장된 토큰이 없습니다. 인증이 필요합니다.',
            'needs_auth': True
        }
    
    try:
        # 토큰 파일을 직접 읽어서 처리 (JavaScript와 호환성을 위해)
        with open(token_path, 'r') as token_file:
            token_data = json.load(token_file)
        # client_id와 client_secret이 없으면 환경 변수에서 추가
        if 'client_id' not in token_data:
            token_data['client_id'] = CLIENT_ID
        if 'client_secret' not in token_data:
            token_data['client_secret'] = CLIENT_SECRET
        creds = Credentials.from_authorized_user_info(token_data, SCOPES)
        
        if creds.valid:
            return {
                'status': 'valid',
                'message': '토큰이 유효합니다.',
                'needs_auth': False
            }
        elif creds.expired and creds.refresh_token:
            # 갱신 가능한지 테스트
            try:
                creds.refresh(Request())
                return {
                    'status': 'refreshed',
                    'message': '토큰이 만료되었지만 갱신되었습니다.',
                    'needs_auth': False
                }
            except Exception:
                return {
                    'status': 'refresh_failed',
                    'message': '토큰 갱신에 실패했습니다. 재인증이 필요합니다.',
                    'needs_auth': True
                }
        else:
            return {
                'status': 'invalid',
                'message': '토큰이 유효하지 않습니다. 재인증이 필요합니다.',
                'needs_auth': True
            }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'토큰 확인 중 오류 발생: {str(e)}',
            'needs_auth': True
        }

def get_credentials():
    """OAuth2 인증을 통해 자격 증명 반환"""
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("환경 변수 GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET 가 필요합니다.")
    
    # 토큰 상태 미리 확인
    token_status = check_token_status()
    print(f"[토큰 상태] {token_status['message']}")
    
    token_path = get_token_path()
    ensure_token_dir()

    creds = None
    if os.path.exists(token_path):
        # 저장된 토큰이 있으면 로드 (JavaScript와 호환성을 위해 직접 읽기)
        try:
            with open(token_path, 'r') as token_file:
                token_data = json.load(token_file)
            # client_id와 client_secret이 없으면 환경 변수에서 추가
            if 'client_id' not in token_data:
                token_data['client_id'] = CLIENT_ID
            if 'client_secret' not in token_data:
                token_data['client_secret'] = CLIENT_SECRET
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # 토큰 파일 형식이 맞지 않으면 None으로 처리하고 재인증
            print(f"[경고] 토큰 파일 형식 오류: {e}. 재인증이 필요합니다.")
            creds = None
    
    if not creds or not creds.valid:
        # 토큰이 없거나 유효하지 않으면 새로 생성
        if creds and creds.expired and creds.refresh_token:
            # 토큰이 만료되었지만 갱신 가능하면 갱신 시도
            try:
                creds.refresh(Request())
            except Exception:
                # 갱신 실패 시 (refresh_token이 만료되었거나 취소된 경우) 새로 인증
                creds = None
        
        if not creds or not creds.valid:
            # 새로 OAuth2 플로우를 통해 인증 (크롬 창이 열림)
            print("[인증 시작] 브라우저가 자동으로 열립니다. 인증을 완료해주세요.")
            
            # 인증 이미지 자동 클릭 설정 (필요할 때만 임포트)
            from modules import re_authModule
            
            script_dir = os.path.dirname(os.path.abspath(__file__))
            auth_image_path_1 = os.path.join(script_dir, "src", "re-auth_img", "1_ID_shin_2.png")
            auth_image_path_1 = os.path.normpath(auth_image_path_1)
            auth_image_path_2 = os.path.join(script_dir, "src", "re-auth_img", "2_continue.png")
            auth_image_path_2 = os.path.normpath(auth_image_path_2)
            auth_image_path_3 = os.path.join(script_dir, "src", "re-auth_img", "3.check_all.png")
            auth_image_path_3 = os.path.normpath(auth_image_path_3)
            auth_image_path_4 = os.path.join(script_dir, "src", "re-auth_img", "4_continue_b.png")
            auth_image_path_4 = os.path.normpath(auth_image_path_4)
            
            # 이미지 클릭을 백그라운드로 실행
            import threading
            def auto_click_auth_image():
                try:
                    # 첫 번째 이미지가 나타날 때까지 기다렸다가 클릭
                    print("[이미지 클릭] 첫 번째 이미지를 기다립니다...")
                    if re_authModule.locate_and_click_by_path(
                        auth_image_path_1,
                        max_retries=120,  # 최대 120초 대기
                        retry_interval=1
                    ):
                        print("[이미지 클릭] 첫 번째 이미지 클릭 완료. 두 번째 이미지를 기다립니다...")
                        # 두 번째 이미지가 나타날 때까지 기다렸다가 클릭
                        if re_authModule.locate_and_click_by_path(
                            auth_image_path_2,
                            max_retries=120,  # 최대 120초 대기
                            retry_interval=1
                        ):
                            print("[이미지 클릭] 두 번째 이미지 클릭 완료. 세 번째 이미지를 기다립니다...")
                            # 세 번째 이미지가 나타날 때까지 기다렸다가 클릭
                            if re_authModule.locate_and_click_by_path(
                                auth_image_path_3,
                                max_retries=120,  # 최대 120초 대기
                                retry_interval=1
                            ):
                                print("[이미지 클릭] 세 번째 이미지 클릭 완료. 네 번째 이미지를 기다립니다...")
                                # 네 번째 이미지가 나타날 때까지 기다렸다가 클릭
                                re_authModule.locate_and_click_by_path(
                                    auth_image_path_4,
                                    max_retries=120,  # 최대 120초 대기
                                    retry_interval=1
                                )
                except Exception as e:
                    print(f"[이미지 클릭] 자동 클릭 중 오류 발생: {e}")
            
            # 백그라운드 스레드로 이미지 클릭 시작
            click_thread = threading.Thread(target=auto_click_auth_image, daemon=True)
            click_thread.start()
            
            flow = InstalledAppFlow.from_client_config(
                {
                    "installed": {
                        "client_id": CLIENT_ID,
                        "client_secret": CLIENT_SECRET,
                        "redirect_uris": ["http://localhost"],
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                    }
                },
                SCOPES
            )
            creds = flow.run_local_server(port=0)
            print("[인증 완료] 토큰이 저장되었습니다.")
        
        # 생성된 토큰을 파일에 저장
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return creds
