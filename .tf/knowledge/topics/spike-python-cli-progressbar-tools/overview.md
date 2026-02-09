# spike-python-cli-progressbar-tools

Research on Python CLI progress bar libraries for adding optional progress display to `tk ralph`.

## Quick Answer

For `tk ralph`, **tqdm** is recommended as the primary choice due to its lightweight nature, minimal dependencies, and excellent logging integration via `logging_redirect_tqdm()`. **Rich** is a strong alternative if visual polish and modern terminal features are prioritized.

## Key Findings

1. **tqdm**: ~60ns/iteration overhead, built-in logging integration, CLI wrapper tool, GPL-3.0 license
2. **Rich**: Prettier output, modular design, requires RichHandler for logging, MIT license
3. **Both** support suppressing console output while preserving file logging
4. **tqdm-loggable** package available for drop-in replacement with rate-limited logging

## Recommendation

Use **tqdm** with `logging_redirect_tqdm()` for the progress bar implementation. It provides:
- Minimal performance impact
- Clean logging integration without overwriting progress bars
- Optional file-only logging mode to suppress terminal output
- Well-established API with extensive documentation
