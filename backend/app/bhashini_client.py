"""
Thin wrapper around the official Bhashini (ULCA/Dhruva) inference APIs.

Flow, per Bhashini's own docs:
  1. Ask the "pipeline config" endpoint which models/services are available
     for the tasks you care about (translation, tts, asr), using your
     userID + ulcaApiKey.
  2. That response hands back a callback URL, an inference API key, and a
     per-language "serviceId" for each supported task.
  3. Use those serviceIds + the inference API key to actually call
     translation / tts / asr on the compute endpoint.

Register for free credentials at: https://bhashini.gov.in/ulca/user/register
"""

import base64
import os
from typing import Optional

import requests

PIPELINE_CONFIG_URL = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
INFERENCE_URL = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"

# Published pipeline ID that bundles ASR + Translation + TTS.
DEFAULT_PIPELINE_ID = "64392f96daac500b55c543cd"


class BhashiniError(Exception):
    """Raised whenever a Bhashini call fails or a language pair isn't supported."""


class BhashiniClient:
    def __init__(
        self,
        user_id: Optional[str] = None,
        ulca_api_key: Optional[str] = None,
        pipeline_id: Optional[str] = None,
    ):
        self.user_id = user_id or os.environ.get("BHASHINI_USER_ID")
        self.ulca_api_key = ulca_api_key or os.environ.get("BHASHINI_ULCA_API_KEY")
        self.pipeline_id = pipeline_id or os.environ.get("BHASHINI_PIPELINE_ID") or DEFAULT_PIPELINE_ID

        if not self.user_id or not self.ulca_api_key:
            raise BhashiniError(
                "Missing BHASHINI_USER_ID / BHASHINI_ULCA_API_KEY. "
                "Set them in your .env file (see .env.example)."
            )

        self._inference_api_key: Optional[str] = os.environ.get("BHASHINI_INFERENCE_API_KEY")
        self._services: dict = {"translation": {}, "tts": {}, "asr": {}}
        try:
            self._load_pipeline_config()
        except Exception as e:
            if not self._inference_api_key:
                raise e
            # Direct inference key available, proceed with direct pipeline inference!
            print("Direct Bhashini Inference Key loaded successfully!")

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def _load_pipeline_config(self) -> None:
        headers = {
            "Content-Type": "application/json",
            "userID": self.user_id,
            "ulcaApiKey": self.ulca_api_key,
        }

        # Query pipeline tasks individually to ensure Bhashini returns valid configurations for each
        for task_type in ["translation", "tts", "asr"]:
            body = {
                "pipelineTasks": [{"taskType": task_type}],
                "pipelineRequestConfig": {"pipelineId": self.pipeline_id},
            }
            try:
                resp = requests.post(PIPELINE_CONFIG_URL, json=body, headers=headers, timeout=30)
                if resp.status_code != 200:
                    continue

                data = resp.json()
                if not self._inference_api_key:
                    try:
                        self._inference_api_key = data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["value"]
                    except (KeyError, TypeError):
                        pass

                for task_config in data.get("pipelineResponseConfig", []):
                    tt = task_config.get("taskType")
                    if tt not in self._services:
                        continue

                    for lang_cfg in task_config.get("config", []):
                        src = lang_cfg.get("language", {}).get("sourceLanguage")
                        service_id = lang_cfg.get("serviceId")
                        if not src or not service_id:
                            continue

                        if tt == "translation":
                            tgt = lang_cfg.get("language", {}).get("targetLanguage")
                            if tgt:
                                self._services["translation"].setdefault(src, {})[tgt] = service_id
                        else:
                            self._services[tt][src] = service_id
            except Exception as e:
                print(f"Warning: Failed to fetch Bhashini {task_type} config: {e}")

    def available_languages(self, task_type: str):
        """task_type: 'translation', 'tts', or 'asr'."""
        if task_type == "translation":
            return {src: list(targets.keys()) for src, targets in self._services["translation"].items()}
        return list(self._services.get(task_type, {}).keys())

    # ------------------------------------------------------------------
    # Compute calls
    # ------------------------------------------------------------------
    def _compute_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": self._inference_api_key,
        }

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        cfg = {"language": {"sourceLanguage": source_lang, "targetLanguage": target_lang}}
        service_id = self._services.get("translation", {}).get(source_lang, {}).get(target_lang)
        if service_id:
            cfg["serviceId"] = service_id

        body = {
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": cfg,
                }
            ],
            "inputData": {"input": [{"source": text}]},
        }

        resp = requests.post(INFERENCE_URL, json=body, headers=self._compute_headers(), timeout=30)
        if resp.status_code != 200:
            raise BhashiniError(f"Translation failed: {resp.status_code} {resp.text}")

        result = resp.json()
        return result["pipelineResponse"][0]["output"][0]["target"]

    def text_to_speech(self, text: str, lang: str, gender: str = "female") -> bytes:
        """Returns raw audio bytes (wav)."""
        cfg = {
            "language": {"sourceLanguage": lang},
            "gender": gender,
            "samplingRate": 8000,
        }
        service_id = self._services.get("tts", {}).get(lang)
        if service_id:
            cfg["serviceId"] = service_id

        body = {
            "pipelineTasks": [
                {
                    "taskType": "tts",
                    "config": cfg,
                }
            ],
            "inputData": {"input": [{"source": text}]},
        }

        resp = requests.post(INFERENCE_URL, json=body, headers=self._compute_headers(), timeout=30)
        if resp.status_code != 200:
            raise BhashiniError(f"TTS failed: {resp.status_code} {resp.text}")

        result = resp.json()
        audio_b64 = result["pipelineResponse"][0]["audio"][0]["audioContent"]
        return base64.b64decode(audio_b64)

    def speech_to_text(self, audio_base64: str, lang: str) -> str:
        """Transcribes base64 encoded audio using Bhashini ASR service."""
        cfg = {
            "language": {"sourceLanguage": lang},
            "audioFormat": "wav",
            "samplingRate": 16000,
        }
        service_id = self._services.get("asr", {}).get(lang)
        if service_id:
            cfg["serviceId"] = service_id

        body = {
            "pipelineTasks": [
                {
                    "taskType": "asr",
                    "config": cfg,
                }
            ],
            "inputData": {"audio": [{"audioContent": audio_base64}]},
        }

        resp = requests.post(INFERENCE_URL, json=body, headers=self._compute_headers(), timeout=30)
        if resp.status_code != 200:
            raise BhashiniError(f"ASR failed: {resp.status_code} {resp.text}")

        result = resp.json()
        return result["pipelineResponse"][0]["output"][0]["source"]


