## What does this add?

<!-- Brief description: what item are you adding/changing and why? -->

## Checklist

- [ ] Item directory is under the correct category (`items/<category>/<name>/`)
- [ ] `manifest.yaml` has all required fields (`id`, `name`, `description`, `category`, `files`)
- [ ] `id` in manifest matches the directory name
- [ ] Scripts output JSON to stdout, errors to stderr
- [ ] Scripts are non-interactive (no prompts)
- [ ] All required env vars are documented in the manifest
- [ ] `AGENTS.md` is included with usage examples
- [ ] Ran `python scripts/validate-item.py items/<category>/<name>/` locally

## Notes

<!-- Anything reviewers should know? Links to the service docs, alternative approaches considered, etc. -->
