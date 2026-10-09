# Setup guide

1. Create or open the public repository named exactly `syedhabibahmadg` under that GitHub account.
2. Copy **all** files, including hidden `.github/workflows/`, into the repository root.
3. Commit and push to `main` (or `master`).
4. In **Settings → Actions → General → Workflow permissions**, enable **Read and write permissions** if the snake workflow needs them.
5. Run **Actions → Update contribution snake → Run workflow**. The first successful run creates the `output` branch and the snake image. Scheduled runs update it daily.
6. Update `config/profile.json` to edit project details or text used by the artwork; run `python scripts/render_assets.py` to regenerate the SVGs and commit the changes.
7. Run `python scripts/render_assets.py --check` and `python scripts/check_readme.py` before pushing.

## Workflows
- `snake.yml`: daily and manual animated contribution snake; writes only to `output`.
- `assets.yml`: checks that generated SVGs match their source config.
- `readme-check.yml`: verifies referenced local images and featured project links.

## Notes
- Project repository links are inherited from the supplied README and were not independently verified online.
- External stat badges and skill icons require their providers to be available.
- GitHub sanitizes scripts and embedded JavaScript, so all visuals are SVG/image-based.
- Do not add secrets or credentials to profile files.
