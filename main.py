import time
from datetime import datetime

import cv2

from record_manager import OUTPUT_DIR, save_record, show_record_summary


# 运动区域小于这个面积时，当作摄像头噪声忽略
MOTION_AREA_THRESHOLD = 1500
AUTO_CAPTURE_INTERVAL = 3.0


def save_image(frame, capture_type: str = "manual") -> None:
    """保存当前画面，并记录截图信息。"""

    OUTPUT_DIR.mkdir(exist_ok=True)

    current_time = datetime.now()
    time_text = current_time.strftime("%Y%m%d_%H%M%S")

    file_name = f"{capture_type}_{time_text}.jpg"
    file_path = OUTPUT_DIR / file_name

    success = cv2.imwrite(str(file_path), frame)

    if success:
        record_success = save_record(
            file_name,
            current_time,
            capture_type,
        )

        if record_success:
            print(f"截图和记录已保存：{file_path}")
        else:
            print(f"截图已保存，但记录写入失败：{file_path}")
    else:
        print("截图保存失败")


def main() -> None:
    """打开摄像头，显示实时画面并检测运动区域。"""

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise RuntimeError("无法打开摄像头，请检查摄像头权限")

    # 保存上一帧经过处理后的灰度图
    previous_gray = None
    last_motion_capture_time = 0.0
    print("摄像头已启动")
    print("按 S 保存截图，按 R 查看记录，按 Q 退出程序")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("无法读取摄像头画面")
                break

            
            # 1. 把彩色画面转换为灰度图
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 2. 模糊画面，减少细小噪声造成的误判
            gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

            motion_detected = False

            # 第一帧没有上一帧，暂时无法比较
            if previous_gray is not None:
                # 3. 计算当前帧和上一帧的差异
                frame_delta = cv2.absdiff(previous_gray, gray_frame)

                # 4. 把差异明显的像素变成白色，其余变成黑色
                _, threshold_frame = cv2.threshold(
                    frame_delta,
                    25,
                    255,
                    cv2.THRESH_BINARY,
                )

                # 5. 扩大白色区域，让零散变化连接起来
                threshold_frame = cv2.dilate(
                    threshold_frame,
                    None,
                    iterations=2,
                )

                # 6. 找出发生变化区域的轮廓
                contours, _ = cv2.findContours(
                    threshold_frame,
                    cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE,
                )

                for contour in contours:
                    area = cv2.contourArea(contour)

                    # 面积太小，大概率只是摄像头噪声
                    if area < MOTION_AREA_THRESHOLD:
                        continue

                    motion_detected = True

                    # 获取包住这个运动区域的矩形
                    x, y, width, height = cv2.boundingRect(contour)

                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x + width, y + height),
                        (0, 0, 255),
                        2,
                    )

            # 当前帧留到下一次循环，成为“上一帧”
            previous_gray = gray_frame

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cv2.putText(
                frame,
                f"GreenLab Twin | {current_time}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

            if motion_detected:
                status_text = "MOTION DETECTED"
                status_color = (0, 0, 255)
            else:
                status_text = "IDLE"
                status_color = (0, 255, 0)

            cv2.putText(
                frame,
                status_text,
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                status_color,
                2,
                cv2.LINE_AA,
            )
            if motion_detected:
                current_motion_time = time.monotonic()

                time_since_last_capture = ( current_motion_time - last_motion_capture_time )

                if time_since_last_capture >= AUTO_CAPTURE_INTERVAL:
                    save_image(frame, "motion")
                    last_motion_capture_time = current_motion_time
            cv2.imshow("GreenLab Twin", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("s"):
                save_image(frame, "manual")
            elif key == ord("r"):
                show_record_summary()
            elif key == ord("q"):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()
        print("程序已安全退出")


if __name__ == "__main__":
    main()