# trychlos:pyjpi

## ChangeLog

### 0.1.30-rc.0

    Release date:

    - Have a debug line before and after the device request

### 0.1.29

    Release date: 2026-09-07

    - Name release workflows by version
    - Restrict releases to stable semantic version tags
    - Debug the returned parsed response

### 0.1.28

    Release date: 2026-09-06

    - Fix release coverage reporting with current setuptools versions
    - Generate the GitHub release name directly from the version tag

### 0.1.27

    Release date: 2026-09-06

    - Add CodeFactor (<https://www.codefactor.io/repository/github/trychlos/pyjpi>)
    - Refactoring: reformat and rename ChangeLog
    - Refactoring: comment out 'maintained=yes' badge
    - Refactoring: update .gitignore
    - Refactoring: .badges/ becomes .github/assets
    - Raise explicit connection and response exceptions instead of returning
      ambiguous false values
    - Validate HTTP status codes and release responses reliably
    - Preserve existing URL query parameters when adding JPI actions
    - Validate device names and battery responses
    - Validate battery levels and boolean values
    - Add typed public battery and HTTP response models

### 0.1.26

    Release date: 2025-09-20

    - Initial release
