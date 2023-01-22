import json
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List

from voicevox_engine.metas.Metas import CoreSpeaker, EngineSpeaker, Speaker

if TYPE_CHECKING:
    from voicevox_engine.synthesis_engine.synthesis_engine_base import (
        SynthesisEngineBase,
    )


class MetasStore:
    """
    話者やスタイルのメタ情報を管理する
    """

    def __init__(self, engine_speakers_path: Path) -> None:
        self._engine_speakers_path = engine_speakers_path
        self._loaded_metas: Dict[str, EngineSpeaker] = {
            folder.name: EngineSpeaker(
                **json.loads((folder / "metas.json").read_text(encoding="utf-8"))
            )
            for folder in engine_speakers_path.iterdir()
        }

    def speaker_engine_metas(self, speaker_uuid: str) -> EngineSpeaker:
        return self.loaded_metas[speaker_uuid]

    def combine_metas(self, core_metas: List[CoreSpeaker]) -> List[Speaker]:
        """
        与えられたmetaにエンジンのコア情報を付加して返す
        core_metas: コアのmetas()が返すJSONのModel
        """

        return [
            Speaker(
                **self.speaker_engine_metas(speaker_meta.speaker_uuid).dict(),
                **speaker_meta.dict(),
            )
            for speaker_meta in core_metas
        ]

    def load_combined_metas(self, engine: "SynthesisEngineBase") -> List[Speaker]:
        """
        与えられたエンジンから、コア・エンジン両方の情報を含んだMetasを返す
        """

        core_metas = [CoreSpeaker(**speaker) for speaker in json.loads(engine.speakers)]
        return self.combine_metas(core_metas)

    @property
    def engine_speakers_path(self) -> Path:
        return self._engine_speakers_path

    @property
    def loaded_metas(self) -> Dict[str, EngineSpeaker]:
        return self._loaded_metas

    @staticmethod
    def metas_to_raw(speakers: List[Speaker]):
        return [speaker.dict() for speaker in speakers]
