OPTIONAL OFFLINE MODELS

Conversational Brain:
- Put one compatible quantized GGUF model in this folder.
- ARLEN detects the first .gguf file.
- Install requirements-ai.txt before enabling local chat.
- For an 8 GB PC, use a small 1.5B–3B Q4 model.

Voice Pack:
- Put the selected offline voice model inside models\voice.
- The base application never keeps the microphone active.

No model is bundled in the source package because model licensing, hardware fit,
and file size must be selected separately.

