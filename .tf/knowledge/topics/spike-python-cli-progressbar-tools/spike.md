# Spike: Python CLI Progress Bar Tools with Logging Integration

## Summary

This spike investigates Python libraries for adding progress bars to CLI tools with specific focus on:
1. Optional progress display (can be disabled)
2. Logging integration (logs appear above progress bar)
3. Terminal output suppression (quiet mode)

## Options Considered

### 1. tqdm (Recommended)

**Overview**: Lightweight progress bar library with ~60ns/iteration overhead.

**Pros**:
- Minimal dependencies (pure Python)
- Built-in `logging_redirect_tqdm()` for clean log integration
- CLI wrapper tool included (`tqdm` command)
- Excellent ETA predictions and smoothing
- Works in Jupyter, terminals, and files
- `tqdm-loggable` package for advanced logging features

**Cons**:
- Visual appearance is basic (no colors by default)
- GPL-3.0 license (vs MIT for Rich)

**Logging Integration**:
```python
import logging
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with logging_redirect_tqdm():
    for i in tqdm(range(100), desc="Processing"):
        logger.info(f"Step {i}")  # Appears above progress bar
```

**Suppressing Terminal Output**:
```python
# Option 1: File-only logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler('ralph.log'),
        # No StreamHandler = no console output
    ]
)

# Option 2: Use tqdm with disable=True
for i in tqdm(range(100), disable=not show_progress):
    process(i)
```

### 2. Rich

**Overview**: Modern terminal library with pretty progress bars and rich text.

**Pros**:
- Beautiful, colorful output
- Modular design (use only what you need)
- `RichHandler` for logging integration
- Live displays and spinners
- MIT license

**Cons**:
- Higher overhead than tqdm
- More complex API for simple use cases
- Requires explicit `progress.print()` instead of `print()`

**Logging Integration**:
```python
import logging
from rich.logging import RichHandler
from rich.progress import Progress

logging.basicConfig(
    level="INFO",
    handlers=[RichHandler(show_level=False)]
)
logger = logging.getLogger(__name__)

with Progress() as progress:
    task = progress.add_task("Processing...", total=100)
    for i in range(100):
        logger.info(f"Step {i}")  # Renders above progress
        progress.update(task, advance=1)
```

### 3. tqdm with Rich Backend

**Overview**: tqdm can use Rich as its rendering backend.

```python
from tqdm.rich import tqdm

# Uses Rich for rendering but tqdm API
for i in tqdm(range(100)):
    process(i)
```

**Note**: Limited nested bar support as of 2024.

## Comparison Matrix

| Feature | tqdm | Rich | tqdm.rich |
|---------|------|------|-----------|
| Overhead | ~60ns/iter | Higher | Higher |
| Dependencies | Minimal | Rich + deps | Rich + deps |
| License | GPL-3.0 | MIT | GPL-3.0 |
| Logging | `logging_redirect_tqdm()` | `RichHandler` | `logging_redirect_tqdm()` |
| Visuals | Basic | Excellent | Excellent |
| ETA Accuracy | Excellent | Good | Excellent |
| CLI Tool | Yes | No | No |

## Recommendation

**Use tqdm** for `tk ralph` because:

1. **Performance**: Minimal overhead is important for a CLI tool that processes many tickets
2. **Simplicity**: Single-purpose library, less complexity
3. **Logging**: `logging_redirect_tqdm()` provides clean integration
4. **Suppression**: Easy to disable progress bar and/or redirect logs to file only

### Suggested Implementation Pattern

```python
import logging
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

def run_ralph(tickets, show_progress=True, quiet=False):
    # Configure logging based on quiet mode
    handlers = [logging.FileHandler('ralph.log')]
    if not quiet:
        handlers.append(logging.StreamHandler())
    
    logging.basicConfig(
        level=logging.INFO,
        handlers=handlers,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # Progress bar with logging integration
    with logging_redirect_tqdm():
        for ticket in tqdm(tickets, desc="Processing tickets", disable=not show_progress):
            logger.info(f"Processing {ticket.id}")
            process_ticket(ticket)
```

## Risks & Unknowns

1. **GPL-3.0 License**: May have implications for distribution. Consider `tqdm-loggable` (MIT) if needed.
2. **Terminal Width**: Long ticket IDs may cause line wrapping. Use `dynamic_ncols=True`.
3. **Nested Progress**: If implementing sub-progress per ticket phase, nested bars need position management.

## Next Steps

1. Add `tqdm` to project dependencies
2. Implement `--progress` / `--no-progress` flags for `tk ralph`
3. Implement `--quiet` flag to suppress console logging
4. Test with actual ticket processing to verify performance
5. Consider `tqdm-loggable` if rate-limited logging is needed
