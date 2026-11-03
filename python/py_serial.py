import serial
import threading
import time
import sys

# 請確認 COM 埠正確
COM_PORT = 'COM6'
BAUD_RATE = 115200

try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    print(f"已成功連線至 {COM_PORT}")
except Exception as e:
    print(f"連線失敗: {e}")
    sys.exit()

def receive_data():
    """ 背景執行緒：負責接收 STM32 回傳的資料 """
    while True:
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    print(f"\r[STM32 回報] {line}\n> ", end="")
            except Exception as e:
                pass
        time.sleep(0.01)

# 啟動接收執行緒
rx_thread = threading.Thread(target=receive_data, daemon=True)
rx_thread.start()

print("=========================================")
print(" 指令說明：")
print(" 1. light X  (設定光照 0~100，例如 light 80)")
print(" 2. water X  (設定水量 0~100，例如 water 50)")
print(" 3. 輸入 exit 離開程式")
print("=========================================")

# 主執行緒：負責發送指令
while True:
    cmd = input("> ")
    if cmd.lower() == 'exit':
        break
    
    if cmd.startswith("light ") or cmd.startswith("water "):
        cmd_send = cmd + "\r\n"
        ser.write(cmd_send.encode('utf-8'))
    else:
        print("格式錯誤，請輸入 'light X' 或 'water X'")

ser.close()
print("通訊結束。")