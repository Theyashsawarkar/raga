# 3. Hand music to nāda, keep rmpc as a fallback

**Status:** Accepted  
**Date:** 2026-10-21

## Context

raga queued music through `rmpc addyt`, which downloads before playing and reports success even when the download failed. nāda now streams YouTube directly and lines up what comes next.

## Decision

Music goes to `nada add --play` (or `--next`) when nāda is installed; otherwise it still goes through rmpc. Video always opens in mpv.

## Consequences

- Music starts in about two seconds, with autoplay, lyrics and downloads.
- `nada_command` lets users choose; an empty value keeps rmpc.
