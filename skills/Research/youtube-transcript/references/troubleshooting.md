# Troubleshooting

## `google-genai` is not installed

Install the dependency in the active Python environment:

```bash
python3 -m venv .venv
.venv/bin/pip install google-genai
```

## `GEMINI_API_KEY` is not set

The script requires a Gemini API key in the process environment.

Options:

```bash
GEMINI_API_KEY="..." .venv/bin/python3 scripts/get_transcript.py "YOUTUBE_URL"
```

or use your secret manager, for example Varlock with a local `.env.schema` adapted from `templates/env.schema.example`:

```bash
varlock run -- .venv/bin/python3 scripts/get_transcript.py "YOUTUBE_URL"
```

Do not print API keys and do not commit `.env` files.

## Varlock validation fails

Run:

```bash
varlock load
```

Then fix the local `.env.schema` entry that failed. The repo only provides a generic template; your local secret manager path may differ.

## Video processing fails

Common causes:

- Video is private, deleted, age-restricted, or geo-blocked.
- Video is too long for the selected model/path.
- Gemini temporarily cannot fetch or process the URL.
- The URL is not a standard YouTube watch, Shorts, or `youtu.be` link.

Verify with a short, public YouTube URL before debugging credentials.

## Model not found

Use a current Gemini model name from Google's model docs and pass it explicitly:

```bash
.venv/bin/python3 scripts/get_transcript.py "YOUTUBE_URL" --model gemini-2.5-flash
```

You can also set:

```bash
GEMINI_MODEL=gemini-2.5-flash
```

## Empty transcript response

Retry once with the same model. If it still fails, try a shorter public video or another Gemini model. Treat repeated empty output as a source/model limitation, not a successful transcript.
