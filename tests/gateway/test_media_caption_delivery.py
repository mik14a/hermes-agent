"""Tests for text+image caption bundling (OpenClaw-style single-message delivery)."""

from gateway.platforms.base import BasePlatformAdapter


class TestPartitionTextAndImageCaption:
    def test_single_image_bundles_on_discord(self):
        text, media, caption = BasePlatformAdapter.partition_text_and_image_caption(
            "みぃ様、お待ちしております。",
            [("/tmp/heartbeat.png", False)],
            platform="discord",
        )
        assert text == ""
        assert caption == "みぃ様、お待ちしております。"
        assert media == [("/tmp/heartbeat.png", False)]

    def test_two_images_keeps_split(self):
        text, media, caption = BasePlatformAdapter.partition_text_and_image_caption(
            "Report",
            [("/tmp/a.png", False), ("/tmp/b.png", False)],
            platform="discord",
        )
        assert text == "Report"
        assert caption is None
        assert len(media) == 2

    def test_voice_not_bundled(self):
        text, media, caption = BasePlatformAdapter.partition_text_and_image_caption(
            "Listen",
            [("/tmp/voice.ogg", False)],
            platform="telegram",
        )
        assert text == "Listen"
        assert caption is None

    def test_telegram_respects_1024_limit(self):
        long_text = "x" * 1025
        text, media, caption = BasePlatformAdapter.partition_text_and_image_caption(
            long_text,
            [("/tmp/a.png", False)],
            platform="telegram",
        )
        assert text == long_text
        assert caption is None

    def test_caption_for_image_batch_multiple(self):
        remaining, caption = BasePlatformAdapter.caption_for_image_batch(
            "Multi chart report",
            ["/tmp/a.png", "/tmp/b.png"],
            platform="discord",
        )
        assert remaining == ""
        assert caption == "Multi chart report"
