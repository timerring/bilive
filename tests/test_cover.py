import unittest
from src.cover.image_model_sdk.amazon_sdk import amazon_generate_cover
from src.cover.image_model_sdk.baidu_sdk import baidu_generate_cover
from src.cover.image_model_sdk.hidream_sdk import hidream_generate_cover
from src.cover.image_model_sdk.ideogram_sdk import ideogram_generate_cover
from src.cover.image_model_sdk.kolors_sdk import kolors_generate_cover
from src.cover.image_model_sdk.luma_sdk import luma_generate_cover
from src.cover.image_model_sdk.minimax_sdk import minimax_generate_cover
from src.cover.image_model_sdk.recraft_sdk import recraft_generate_cover
from src.cover.image_model_sdk.stability_sdk import stable_diffusion_generate_cover
from src.cover.image_model_sdk.tencent_sdk import hunyuan_generate_cover
from src.cover.image_model_sdk.kling_sdk import kling_generate_cover

class BaseTest(unittest.TestCase):
    file_path = ""


class TestAmazonMain(BaseTest):
    def test_amazon_generate_cover(self):
        cover_path = amazon_generate_cover(self.file_path)
        self.assertIsNotNone(cover_path)
        print(cover_path, flush=True)


class TestBaiduMain(BaseTest):
    def test_baidu_generate_cover(self):
        cover_path = baidu_generate_cover(self.file_path)
        self.assertIsNotNone(cover_path)
        print(cover_path, flush=True)

class TestHidreamMain(BaseTest):
    def test_hidream_generate_cover(self):
        cover_path = hidream_generate_cover(self.file_path)
        self.assertIsNotNone(cover_path)
        print(cover_path, flush=True)

class TestIdeogramMain(BaseTest):
    def test_ideogram_generate_cover(self):
        cover_path = ideogram_generate_cover(self.file_path)
        self.assertIsNotNone(cover_path)
        print(cover_path, flush=True)

class TestKolorsMain(BaseTest):
    def test_kolors_generate_cover(self):
        cover_path = kolors_generate_cover(self.file_path)
        self.assertIsNotNone(cover_path)
        print(cover_path, flush=True)

class TestLumaMain(BaseTest):
    def test_luma_generate_cover(self):
        cover_path = luma_generate_cover(self.file_path)
        self.assertIsNotNone(cover_path)
        print(cover_path, flush=True)

class TestMinimaxMain(BaseTest):
    def test_minimax_generate_cover(self):
        cover_path = minimax_generate_cover(self.file_path)
        self.assertIsNotNone(cover_path)
        print(cover_path, flush=True)

class TestRecraftMain(BaseTest):
    def test_recraft_generate_cover(self):
        cover_path = recraft_generate_cover(self.file_path)
        self.assertIsNotNone(cover_path)
        print(cover_path, flush=True)

class TestStabilityMain(BaseTest):
    def test_stable_diffusion_generate_cover(self):
        cover_path = stable_diffusion_generate_cover(self.file_path)
        self.assertIsNotNone(cover_path)
        print(cover_path, flush=True)

class TestTencentMain(BaseTest):
    def test_hunyuan_generate_cover(self):
        cover_path = hunyuan_generate_cover(self.file_path)
        self.assertIsNotNone(cover_path)
        print(cover_path, flush=True)

class TestKlingMain(BaseTest):
    def test_kling_generate_cover(self):
        cover_path = kling_generate_cover(self.file_path)
        self.assertIsNotNone(cover_path)
        print(cover_path, flush=True)

if __name__ == "__main__":
    unittest.main()
