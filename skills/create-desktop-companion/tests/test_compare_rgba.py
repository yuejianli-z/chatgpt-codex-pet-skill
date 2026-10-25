import importlib.util
from pathlib import Path
import tempfile
import unittest

from PIL import Image
from PIL.PngImagePlugin import PngInfo

spec = importlib.util.spec_from_file_location(
    'compare_rgba', Path(__file__).resolve().parents[1] / 'scripts/compare_rgba.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class DecodedReadback(unittest.TestCase):
    def compare_images(self, first, second, metadata=False):
        with tempfile.TemporaryDirectory() as temp:
            a, b = Path(temp) / 'source.png', Path(temp) / 'readback.png'
            first.save(a, compress_level=0)
            info = PngInfo()
            if metadata:
                info.add_text('test', 'Synthetic re-encoding; no production asset')
            second.save(b, compress_level=9, pnginfo=info)
            return m.compare(a, b)

    def test_reencoded_png_retains_all_rgba(self):
        image = Image.new('RGBA', (8, 6), (20, 30, 40, 255))
        image.putpixel((2, 3), (70, 80, 90, 0))
        result = self.compare_images(image, image, metadata=True)
        self.assertFalse(result['encoded_bytes_equal'])
        self.assertNotEqual(*result['encoded_sha256'].values())
        self.assertTrue(result['rgba_equal'])
        self.assertEqual(result['changed_pixels'], 0)
        self.assertEqual(set(result['maximum_channel_difference'].values()), {0})
        self.assertFalse(result['runtime_verified'])

    def test_rgb_only_changes_are_not_hidden_by_equal_alpha(self):
        for alpha in (0, 255):
            with self.subTest(alpha=alpha):
                first = Image.new('RGBA', (4, 4), (20, 30, 40, alpha))
                second = first.copy()
                second.putpixel((1, 2), (21, 30, 40, alpha))
                result = self.compare_images(first, second)
                self.assertFalse(result['rgba_equal'])
                self.assertEqual(result['changed_pixels'], 1)
                self.assertEqual(result['maximum_channel_difference'], {'R': 1, 'G': 0, 'B': 0, 'A': 0})

    def test_alpha_only_change_is_detected(self):
        first = Image.new('RGBA', (4, 4), (20, 30, 40, 255))
        second = first.copy()
        second.putpixel((1, 2), (20, 30, 40, 254))
        result = self.compare_images(first, second)
        self.assertFalse(result['rgba_equal'])
        self.assertEqual(result['changed_pixels'], 1)
        self.assertEqual(result['maximum_channel_difference'], {'R': 0, 'G': 0, 'B': 0, 'A': 1})

    def test_size_mismatch_is_not_resized_or_accepted(self):
        result = self.compare_images(Image.new('RGBA', (3, 4)), Image.new('RGBA', (4, 3)))
        self.assertFalse(result['dimensions_equal'])
        self.assertFalse(result['rgba_equal'])
        self.assertIsNone(result['changed_pixels'])
        self.assertIsNone(result['maximum_channel_difference'])

    def test_unsupported_precision_and_animation_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            a, b = Path(temp) / 'source.png', Path(temp) / 'readback.png'
            with self.subTest(input='16-bit'):
                Image.new('I;16', (4, 4), 1000).save(a)
                Image.new('I;16', (4, 4), 2000).save(b)
                with self.assertRaisesRegex(ValueError, 'single-frame 8-bit'):
                    m.compare(a, b)
            with self.subTest(input='animated PNG'):
                Image.new('RGBA', (4, 4), 'red').save(
                    a, save_all=True, append_images=[Image.new('RGBA', (4, 4), 'blue')])
                Image.new('RGBA', (4, 4), 'red').save(b)
                with self.assertRaisesRegex(ValueError, 'single-frame 8-bit'):
                    m.compare(a, b)


if __name__ == '__main__':
    unittest.main()
