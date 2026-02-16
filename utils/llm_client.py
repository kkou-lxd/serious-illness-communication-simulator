"""Generic LLM client wrapper for Azure OpenAI endpoints."""

from __future__ import annotations

import os
from typing import Dict, Optional

import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI, OpenAIError

load_dotenv()


class LLMConfigurationError(RuntimeError):
    """Raised when required LLM configuration is missing."""


def _safe_secret_get(key_name: str) -> str | None:
    """Read a Streamlit secret without crashing when secrets are not configured."""
    try:
        value = st.secrets.get(key_name)
    except Exception:
        return None
    return str(value) if value else None


def _get_auto_credentials() -> Dict[str, str]:
    """
    Auto-load Azure credentials with priority:
    1) Streamlit secrets (cloud)
    2) Environment variables / .env (local)
    """

    def resolve(key_name: str) -> str:
        return _safe_secret_get(key_name) or os.getenv(key_name, "")

    return {
        "azure_api_key": resolve("AZURE_OPENAI_API_KEY"),
        "azure_endpoint": resolve("AZURE_OPENAI_ENDPOINT"),
        "azure_deployment": resolve("AZURE_OPENAI_DEPLOYMENT_NAME"),
        "azure_api_version": resolve("AZURE_API_VERSION"),
    }


def _valid_azure_config(azure_config: Optional[Dict[str, str]]) -> bool:
    if not azure_config:
        return False
    required = ["azure_api_key", "azure_endpoint", "azure_deployment", "azure_api_version"]
    return all(azure_config.get(k) for k in required)


def call_llm(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.3,
    max_tokens: int = 1024,
    azure_config: Optional[Dict[str, str]] = None,
) -> str:
    """
    Generic LLM call that sends prompts to an Azure-compatible endpoint.

    If `azure_config` is missing, credentials are auto-loaded from Streamlit
    secrets first, then environment variables.
    """
    current_config = azure_config or _get_auto_credentials()

    if not _valid_azure_config(current_config):
        return "System not configured. Please ask the instructor to set up the AI connection."

    try:
        client = AzureOpenAI(
            api_key=current_config["azure_api_key"],
            api_version=current_config["azure_api_version"],
            azure_endpoint=current_config["azure_endpoint"],
        )
        completion = client.chat.completions.create(
            model=current_config["azure_deployment"],
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = completion.choices[0].message.content
        return content.strip() if content else ""
    except OpenAIError:
        return "System not configured. Please ask the instructor to set up the AI connection."


def _mock_response(user_prompt: str) -> str:
    """Return an empty mock response to avoid polluting UI when LLM is not configured."""
    return ""


__all__ = ["call_llm", "LLMConfigurationError"]
