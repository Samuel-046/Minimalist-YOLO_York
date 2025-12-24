# 核心函式庫
import time
import cv2
from ultralytics import YOLO
import win32com.client as win32 # 替換 pyttsx3 的新語音庫

# --- 配置參數 ---
MODEL_PATH = 'yolov8n.pt' 
SPEECH_COOLDOWN = 4 
CONFIDENCE_THRESHOLD = 0.5 

# --- 初始化 ---
print("--- 系統初始化開始 ---")
print("1. Loading YOLO Model...")
try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"ERROR: Failed to load YOLO model: {e}")
    exit()
print("   > Model loaded successfully.")

print("2. Initializing Text-to-Speech Engine (win32com)...")
speaker = None
try:
    # 使用 win32com.client 創建語音物件
    speaker = win32.Dispatch("SAPI.SpVoice")
    # speaker.Rate = 0 # 語速 (0為預設)
    # speaker.Volume = 100 # 音量
except Exception as e:
    print(f"ERROR: win32com 語音初始化失敗: {e}")
    speaker = None 
print("   > Speech engine initialized.")


print("3. Setting up Webcam...")
cap = cv2.VideoCapture(0) 
if not cap.isOpened():
    print("ERROR: Could not open webcam. Check if another program is using it.")
    exit()
print("   > Webcam opened successfully.")


# 語音頻率控制變數
last_spoken_object = "" 
last_spoken_time = time.time() 

print("-" * 40)
print("系統就緒。請按 'q' 鍵退出即時偵測視窗。")
print("-" * 40)

# --- 主偵測循環 ---

try:
    while cap.isOpened():
        
        success, frame = cap.read()
        if not success:
            print("Failed to read frame from webcam.")
            break

        # 執行 YOLO 偵測
        results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False) 
        current_time = time.time()

        if results and len(results[0].boxes) > 0:
            first_box = results[0].boxes[0]
            class_name = model.names[int(first_box.cls)]
            
            # 語音回饋邏輯
            # win32com 的語音呼叫是同步的，所以我們只檢查冷卻時間
            if (speaker is not None) and \
               (class_name != last_spoken_object or current_time - last_spoken_time > SPEECH_COOLDOWN):
                
                text_to_speak = f"Alert! I see a {class_name}."
                
                print(f"[{time.strftime('%H:%M:%S')}] Speaking: {text_to_speak}")
                
                # 關鍵：同步呼叫語音，但由於 SAPI 的優化，不會鎖死 OpenCV
                speaker.Speak(text_to_speak, 1) # 1: SVSFlagsAsync 異步模式
                
                last_spoken_object = class_name
                last_spoken_time = current_time

        # 顯示結果
        annotated_frame = results[0].plot()
        cv2.imshow("YOLO Live Identifier (Press 'q' to quit)", annotated_frame)
        
        # 檢查退出指令
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        
        # 讓出 CPU 時間
        time.sleep(0.001) 

except Exception as e:
    print(f"\nCaught Main Loop Error: {e}")

finally:
    # 釋放資源
    if 'cap' in locals():
        cap.release()
    cv2.destroyAllWindows()
    # win32com.client 不需要 engine.stop()
    print("--- 系統資源已釋放。---")

