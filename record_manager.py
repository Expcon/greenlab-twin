import json
from datetime import datetime
from pathlib import Path


OUTPUT_DIR = Path("outputs")
RECORD_FILE = OUTPUT_DIR / "capture_records.json"


def load_records() -> list[dict[str, str]] | None:
    """读取截图记录；读取失败时返回 None。"""

    if not RECORD_FILE.exists():
        return []

    try:
        with RECORD_FILE.open("r", encoding="utf-8") as file:
            records = json.load(file)
    except json.JSONDecodeError:
        print(f"记录文件格式错误：{RECORD_FILE}")
        return None

    if not isinstance(records, list):
        print(f"记录文件的数据结构错误：{RECORD_FILE}")
        return None

    return records


def save_record(
    file_name: str,
    capture_time: datetime,
    capture_type: str,
) -> bool:
    """把截图名称、拍摄时间和截图类型写入 JSON 文件。"""

    records = load_records()

    if records is None:
        return False

    new_record = {
        "file_name": file_name,
        "capture_time": capture_time.strftime("%Y-%m-%d %H:%M:%S"),
        "capture_type": capture_type,
    }

    records.append(new_record)

    OUTPUT_DIR.mkdir(exist_ok=True)

    with RECORD_FILE.open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)

    return True


def show_record_summary() -> None:
    """读取 JSON 文件并显示截图统计。"""

    records = load_records()

    if records is None:
        return

    if not records:
        print("暂时没有截图记录")
        return

    manual_count = 0
    motion_count = 0

    for record in records:
        capture_type = record.get("capture_type", "manual")

        if capture_type == "motion":
            motion_count += 1
        else:
            manual_count += 1

    total_count = len(records)
    latest_record = records[-1]

    latest_file = latest_record.get("file_name", "未知")
    latest_time = latest_record.get("capture_time", "未知")
    latest_type = latest_record.get("capture_type", "manual")

    print(f"当前共保存 {total_count} 张截图")
    print(f"手动截图：{manual_count} 张")
    print(f"运动截图：{motion_count} 张")
    print(f"最近截图：{latest_file}")
    print(f"截图时间：{latest_time}")
    print(f"截图类型：{latest_type}")