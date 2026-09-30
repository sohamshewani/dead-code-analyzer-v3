## Dead Code Analyzer

A command-line utility for analyzing source code to detect dead code, caching the results in an SQLite database, and concurrently testing API performance impact of removing dead code.

### Installation

```bash
pip install dead-code-analyzer
```

### Usage

```bash
dead-code-analyzer analyze --cache --concurrency 5 file1.py file2.py
```

```bash
dead-code-analyzer stress_test
```

### Core Logic

- **analyze_code(filename: str) -> str**: Analyzes the provided Python file for dead code using an AST-based approach.
- **cache_analysis_result(filename: str, result: str)**: Caches the analysis result in an SQLite database.
- **get_analysis_result(filename: str) -> str**: Retrieves the cached analysis result.

### CLI Interface

- **analyze**: Analyzes files and caches results.
- **stress_test**: Stress tests API performance with concurrent requests.

### Requirements

- `click`
- `rich`
- `astroid`
- `sqlite3`
- `aiohttp`
- `async-timeout`

### Testing

The `tests` directory contains pytest suites for core functionality.