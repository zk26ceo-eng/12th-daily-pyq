# 12th Daily PYQ

A stream-aware Class XII daily-question system for CBSE and a transparent starter library for five Indian state boards. It is designed for students, study groups, and integration into a friend’s web app 

## Current status

The CBSE bank is **COMPLETED**. It was acquired and analyzed from official CBSE material in the existing CBSE PYQ Brain workspace. This repository does not re-extract or duplicate that corpus; see [`pyq-bank/cbse/COMPLETED.md`](pyq-bank/cbse/COMPLETED.md).

State-board work has started for CGBSE Chhattisgarh, UPMSP Uttar Pradesh, MSBSHSE Maharashtra, BSEB Bihar, and MPBSE Madhya Pradesh. Official URLs and availability gaps are recorded under [`pyq-bank/state-boards/`](pyq-bank/state-boards/). Empty question URLs mean that no verifiable official source was found in this pass; they are not silent substitutions.

## Student flow

The onboarding flow has three steps. The student selects a stream, chooses five or six subjects from that stream, and sets language, board, daily time, and questions-per-day preferences. English is compulsory in the supplied profiles. The scheduler never sends a subject that is absent from the saved preferences. For Painting, Music, Physical Education, and similar skill subjects, the daily item is a short one-mark or practical tip rather than a long theory question.

The daily system produces one PYQ per selected subject, includes the repeat year when available, uses English, Hindi, or Hinglish as selected, and ends with `Reply with answers 1-5`. The answer checker marks each response, gives a two-line correction, and places wrong questions on the next repeat list. Doubt explanations use three or four simple lines and one example.

## Run locally

```bash
cp .env.example .env
npm install node-cron
node backend/scheduler.js
```

The scheduler contains a placeholder `sendMessage` function. It does not contain WhatsApp credentials and does not call a real messaging API. Connect that function to The Network or an approved WhatsApp provider after handling consent, opt-outs, rate limits, and message-template rules.

## Contributing PYQs

Add only a source with a verifiable board URL. Put its metadata in the relevant board manifest, preserve the original URL, and add extracted rows to that board’s CSV. Do not label a model paper as an annual PYQ. Use `official-source-unavailable` when a board page cannot be verified.

## State-board scope for this pass

The five-board starter pass prioritizes CGBSE, UPMSP, MSBSHSE, BSEB, and MPBSE. Each board has a latest sample/model-paper link, a marking-scheme or answer-key link when located, five main-subject columns, and five-year rows for 2021–2025. The official archive is uneven: Maharashtra exposes several official HSC papers, Bihar exposes a verified 2025 set, and the other official sites expose mostly model/sample material or opaque archives. See each board README for the exact limitation.

## Integration with The Network

The Network can read `subjects/*.json` during onboarding, store the object described by `backend/user-prefs-template.json`, and call the prompt templates in `prompts/`. The scheduler’s output can be adapted to a WhatsApp message, a community bot, or an in-app daily feed. Keep the question bank and messaging credentials in separate services.
