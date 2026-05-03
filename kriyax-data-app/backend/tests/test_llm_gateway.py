def test_anthropic_sdk_base_url_normalization_for_default_and_custom_endpoints():
    from app.llm.providers.anthropic import _sdk_base_url

    assert _sdk_base_url("https://api.anthropic.com/v1") == "https://api.anthropic.com"
    assert _sdk_base_url("https://api.kimi.com/coding/v1/messages") == "https://api.kimi.com/coding"
    assert _sdk_base_url("https://api.kimi.com/coding/") == "https://api.kimi.com/coding"


def test_openai_compatible_sdk_base_url_normalization_for_kimi_and_azure():
    from app.llm.providers.openai import _sdk_base_url

    assert _sdk_base_url("https://api.openai.com/v1") == "https://api.openai.com/v1"
    assert _sdk_base_url("https://api.kimi.com/coding/v1/chat/completions") == "https://api.kimi.com/coding/v1"
    assert (
        _sdk_base_url("https://example.openai.azure.com")
        == "https://example.openai.azure.com/openai/v1"
    )
