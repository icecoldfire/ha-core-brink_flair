This repository contains a Home Assistant Core integration for Brink Flair.

Copy these paths into a `home-assistant/core` checkout when preparing a PR:

- `homeassistant/components/brink_flair/` → `homeassistant/components/brink_flair/`
- `tests/components/brink_flair/` → `tests/components/brink_flair/`

Notes:

- Replace `@your-github-handle` in `manifest.json` with the real contributor handle.
- The manifest pins `brink-flair-modbus==0.1.0`; publish that package to PyPI or otherwise satisfy Home Assistant's requirement checks before opening the PR.
- Run the normal Home Assistant tooling (`script/setup`, hassfest, pytest, linting, translations) inside a real `home-assistant/core` checkout before submission.
