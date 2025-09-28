import multiprocessing
from multiprocessing import Queue
from queue import Empty
import time
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from core.app_config import AppConfig

# Bộ đếm chia sẻ đơn giản
class ShareCounter:
    def __init__(self, verbose=False, share_value=None):
        self.value = multiprocessing.Value('i', 0)
        self.verbose = verbose
        self.share_value = share_value

    def increase(self):
        with self.value.get_lock():
            self.value.value += 1
            if self.verbose:
                print(f"ShareCounter: {self.value.value}")

# Worker xử lý nhận diện cảm xúc
def analysis_worker(string_queue:Queue, sentiment_queue:Queue):
    tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
    sentiment_model = AutoModelForSequenceClassification.from_pretrained("wonrax/phobert-base-vietnamese-sentiment")
    sentiment_model.to(AppConfig.device).eval()
    print(f"Đã load xong model nhận diện cảm xúc")

    while True:
        try:
            item = string_queue.get(timeout=1)
            if item is None:
                break
        except Empty:
            continue
        request_id, text = item

        start_time = time.perf_counter()  # Bắt đầu đo thời gian

        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=256
        ).to(AppConfig.device)

        with torch.no_grad():
            logits = sentiment_model(**inputs).logits

        probs = torch.softmax(logits, dim=-1).squeeze().tolist()
        id2label = sentiment_model.config.id2label
        pred_idx = int(torch.argmax(logits, dim=-1).item())
        pred_label = id2label[pred_idx]
        pred_confidence = probs[pred_idx] * 100

        elapsed = (time.perf_counter() - start_time) * 1000  # Tính bằng millisecond

        result = (
            f"[{request_id}] Sentiment: {pred_label} ({pred_confidence:.1f}%) "
            f"| Time: {elapsed:.2f} ms"
        )
        sentiment_queue.put((request_id, pred_label))
        print(f"[analysis_worker] {result}")
    sentiment_queue.put(None)

# Phần main chạy tiến trình và gửi dữ liệu
# if __name__ == '__main__':
#     multiprocessing.set_start_method("spawn")  # Bắt buộc trên Windows/Jupyter

#     string_queue = multiprocessing.Queue()
#     share_value = multiprocessing.Value('i', 0)

#     # Tạo tiến trình worker
#     worker = multiprocessing.Process(target=analysis_worker, args=(string_queue, share_value))
#     worker.start()

#     # Gửi test input
#     string_queue.put((time.time(), "Tôi rất thích học về trí tuệ nhân tạo"))
#     string_queue.put((time.time(), "Tôi cảm thấy buồn và thất vọng"))

#     time.sleep(5)  # Chờ model xử lý

#     # Gửi tín hiệu dừng
#     string_queue.put(None)
#     worker.join()
