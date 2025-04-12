import unittest
from src.autoslice.mllm_sdk.sensenova_sdk import sensenova_generate_title
from src.autoslice.mllm_sdk.qwen_sdk import qwen_generate_title

# from src.autoslice.mllm_sdk.gemini_new_sdk import gemini_generate_title
from src.autoslice.mllm_sdk.gemini_old_sdk import gemini_generate_title
from src.autoslice.mllm_sdk.zhipu_sdk import zhipu_glm_4v_plus_generate_title


class BaseTest(unittest.TestCase):
    file_path = "your_video_path"
    artist = "your_artist"


class TestGeminiMain(BaseTest):
    def test_gemini_generate_title(self):
        title = gemini_generate_title(self.file_path, self.artist)
        self.assertIsNotNone(title)


class TestQwenMain(BaseTest):
    def test_qwen_generate_title(self):
        title = qwen_generate_title(self.file_path, self.artist)
        self.assertIsNotNone(title)


class TestSenseNovaMain(BaseTest):
    def test_sensenova_generate_title(self):
        title = sensenova_generate_title(self.file_path, self.artist)
        self.assertIsNotNone(title)


class TestZhipuMain(BaseTest):
    def test_zhipu_generate_title(self):
        title = zhipu_glm_4v_plus_generate_title(self.file_path, self.artist)
        self.assertIsNotNone(title)


if __name__ == "__main__":
    unittest.main()
