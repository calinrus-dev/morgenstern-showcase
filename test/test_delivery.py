import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "samples"))
from media_gate import MediaValidationError, validate_report, probe_media
from delivery_demo import make_epub, make_tone


def report(duration="1.0", types=("audio",)):
    return {"format": {"duration": duration}, "streams": [{"codec_type": t} for t in types]}


class DeliveryTests(unittest.TestCase):
    def test_rejects_non_finite_empty_negative_and_boolean_durations(self):
        for duration in ["NaN", "Infinity", "-Infinity", "", "0", "-1", None, True]:
            with self.subTest(duration=duration), self.assertRaises(MediaValidationError):
                validate_report(report(duration), "audio")

    def test_strict_minimum_boundary(self):
        self.assertEqual(validate_report(report("1.001"), "audio", 1), 1.001)
        with self.assertRaises(MediaValidationError):
            validate_report(report("1"), "audio", 1)

    def test_invalid_reports_and_policy(self):
        for value in [[], {}, {"streams": [1]}, {"streams": [], "format": {"duration": "2"}}]:
            with self.subTest(value=value), self.assertRaises(MediaValidationError):
                validate_report(value, "audio")
        for minimum in [-1, math.nan, math.inf]:
            with self.assertRaises(MediaValidationError):
                validate_report(report(), "audio", minimum)
        with self.assertRaises(MediaValidationError):
            validate_report(report(), "unknown")

    def test_video_requires_audio_by_delivery_policy(self):
        self.assertEqual(validate_report(report(types=("audio", "video")), "video"), 1)
        with self.assertRaises(MediaValidationError):
            validate_report(report(types=("video",)), "video")

    def test_probe_errors_and_timeout(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "fake.wav"
            p.write_bytes(b"fixture")
            for result in [subprocess.CompletedProcess([], 1, "", "bad"), subprocess.CompletedProcess([], 0, "not-json", "")]:
                with patch("media_gate.subprocess.run", return_value=result), self.assertRaises(MediaValidationError):
                    probe_media(p, "audio")
            with patch("media_gate.subprocess.run", side_effect=subprocess.TimeoutExpired("ffprobe", 20)), self.assertRaises(MediaValidationError):
                probe_media(p, "audio")

    def test_epub_structure_and_determinism(self):
        with tempfile.TemporaryDirectory() as d:
            p, q = Path(d) / "a.epub", Path(d) / "b.epub"
            make_epub(p)
            make_epub(q)
            self.assertEqual(p.read_bytes(), q.read_bytes())
            with zipfile.ZipFile(p) as z:
                self.assertEqual(z.namelist()[0], "mimetype")
                self.assertEqual(z.getinfo("mimetype").compress_type, zipfile.ZIP_STORED)
                self.assertEqual(z.read("mimetype"), b"application/epub+zip")
                for entry in z.infolist():
                    self.assertEqual(entry.create_system, 3)
                    self.assertEqual(entry.external_attr >> 16, 0o100644)
                for item in z.namelist()[1:]:
                    ET.fromstring(z.read(item))
                package = ET.fromstring(z.read("EPUB/package.opf"))
                ns = {"o": "http://www.idpf.org/2007/opf"}
                manifest = {e.attrib["id"]: e.attrib["href"] for e in package.findall("o:manifest/o:item", ns)}
                for entry in package.findall("o:spine/o:itemref", ns):
                    self.assertIn("EPUB/" + manifest[entry.attrib["idref"]], z.namelist())

    def test_real_ffprobe_accepts_generated_wave(self):
        self.assertIsNotNone(shutil.which("ffprobe"), "Install FFmpeg/ffprobe to run the integration test")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "tone.wav"
            make_tone(p)
            actual = probe_media(p, "audio", .9)
            self.assertTrue(actual["ok"])
            self.assertAlmostEqual(actual["duration_seconds"], 1)
            p.write_bytes(b"not media")
            with self.assertRaises(MediaValidationError):
                probe_media(p, "audio")


if __name__ == "__main__":
    unittest.main()
