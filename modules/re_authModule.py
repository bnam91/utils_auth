"""
이미지 기반 자동 클릭 모듈
3. 이체집행+시트순서변경까지.py의 이미지 찾기 로직을 모듈화
"""
import pyautogui
import time
import cv2
import numpy as np
import mss
import os

def get_monitor_configs():
    """모니터 설정을 동적으로 가져옵니다."""
    with mss.mss() as sct:
        monitors = []
        for i, monitor in enumerate(sct.monitors[1:], 1):  # monitors[0]은 전체 화면이므로 제외
            monitors.append({
                'top': monitor['top'],
                'left': monitor['left'],
                'width': monitor['width'],
                'height': monitor['height'],
                'number': i
            })
        return monitors

def capture_screen(region):
    """지정된 영역의 화면을 캡처합니다."""
    with mss.mss() as sct:
        screenshot = sct.grab(region)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

def match_template(screen, template_path):
    """템플릿 매칭을 수행합니다."""
    # 한글 경로 지원을 위해 numpy를 사용하여 이미지 로드
    if not os.path.exists(template_path):
        raise ValueError(f"이미지를 찾을 수 없습니다: {template_path}")
    
    template = cv2.imdecode(np.fromfile(template_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if template is None:
        raise ValueError(f"이미지를 로드할 수 없습니다: {template_path}")

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val >= 0.98:  # 일치율이 98% 이상인 경우
        return (max_loc[0] + template.shape[1] // 2, max_loc[1] + template.shape[0] // 2)
    return None

def locate_image_on_monitor(image_path, monitor):
    """단일 모니터에서 이미지를 찾습니다."""
    screen = capture_screen(monitor)
    location = match_template(screen, image_path)
    if location:
        location = (location[0] + monitor['left'], location[1] + monitor['top'])
    return location

def locate_image_on_monitors(image_path):
    """모든 감지된 모니터에서 이미지를 찾습니다."""
    monitors = get_monitor_configs()
    for monitor in monitors:
        location = locate_image_on_monitor(image_path, monitor)
        if location:
            return location
    return None

def locate_and_click_by_path(image_path, max_retries=30, retry_interval=1, wait_before=0):
    """
    이미지 경로를 직접 받아서 찾고 클릭하는 함수
    
    Args:
        image_path: 찾을 이미지의 전체 경로
        max_retries: 최대 재시도 횟수
        retry_interval: 재시도 간격 (초)
        wait_before: 클릭 전 대기 시간 (초)
    
    Returns:
        bool: 이미지를 찾아서 클릭했으면 True, 실패하면 False
    """
    print(f"[이미지 클릭] {os.path.basename(image_path)}을(를) 찾고 클릭합니다.")
    
    # 경로 정규화
    image_path = os.path.normpath(image_path)
    
    if not os.path.exists(image_path):
        print(f"[이미지 클릭] 이미지 파일을 찾을 수 없습니다: {image_path}")
        return False
    
    for attempt in range(max_retries):
        location = locate_image_on_monitors(image_path)
        if location:
            print(f"[이미지 클릭] 이미지를 찾았습니다: {location}, 클릭합니다. (시도 {attempt+1}/{max_retries})")
            if wait_before > 0:
                time.sleep(wait_before)
            pyautogui.click(location)
            time.sleep(0.5)  # 클릭 후 짧은 대기
            return True
        else:
            if attempt < max_retries - 1:  # 마지막 시도가 아니면
                print(f"[이미지 클릭] 이미지를 찾을 수 없습니다. (시도 {attempt+1}/{max_retries})")
                time.sleep(retry_interval)
    
    print(f"[이미지 클릭] {max_retries}회 시도 후에도 이미지를 찾을 수 없었습니다.")
    return False

def click_image_after_delay(image_path, delay_seconds=5, max_retries=30, retry_interval=1):
    """
    지정된 시간 후에 이미지를 찾아서 클릭하는 함수
    
    Args:
        image_path: 찾을 이미지의 전체 경로
        delay_seconds: 클릭 전 대기 시간 (초)
        max_retries: 최대 재시도 횟수
        retry_interval: 재시도 간격 (초)
    
    Returns:
        bool: 이미지를 찾아서 클릭했으면 True, 실패하면 False
    """
    print(f"[이미지 클릭] {delay_seconds}초 후에 이미지를 찾아 클릭합니다...")
    time.sleep(delay_seconds)
    return locate_and_click_by_path(image_path, max_retries, retry_interval)

