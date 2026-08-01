from datetime import datetime
from pathlib import Path

import cv2
import json


OUTPUT_DIR = Path("outputs")
RECORD_FILE = OUTPUT_DIR / "capture_records.json"

def save_record(file_name: str, capture_time: datetime) -> None:
    """把截图名称和拍摄时间写入 JSON 文件。"""

    records = []

    if RECORD_FILE.exists():
        with RECORD_FILE.open("r", encoding="utf-8") as file:
            records = json.load(file)

    new_record = {
        "file_name": file_name,
        "capture_time": capture_time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    records.append(new_record)

    with RECORD_FILE.open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)

def save_image(frame) -> None:
    """将当前摄像头画面保存到 outputs 文件夹。"""

    OUTPUT_DIR.mkdir(exist_ok=True)

    current_time = datetime.now()
    file_name = current_time.strftime("capture_%Y%m%d_%H%M%S.jpg")
    file_path = OUTPUT_DIR / file_name

    success = cv2.imwrite(str(file_path), frame)

    if success:
        save_record(file_name, current_time)
        print(f"截图已保存：{file_path}")
    else:
        print("截图保存失败")


def main() -> None:
    """打开摄像头并显示实时画面。"""

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise RuntimeError("无法打开摄像头，请检查摄像头权限")

    print("摄像头已启动")
    print("按 S 保存截图，按 Q 退出程序")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("无法读取摄像头画面")
                break

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cv2.putText(
                frame,
                f"GreenLab Twin | {current_time}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

            cv2.imshow("GreenLab Twin", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("s"):
                save_image(frame)
            elif key == ord("q"):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()
        print("程序已安全退出")


if __name__ == "__main__":
    main()