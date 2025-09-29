# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a book creation agent that generates books from given instructions and information. The project follows a three-phase workflow: draft creation, image generation using Google nanobanana API, and final book compilation.

## Architecture and Workflow

The system follows this processing flow:

1. **Input Phase**: Receive instructions and information, validate completeness
2. **Draft Phase**: Create structure proposal, generate markdown files per chapter with image placeholders
3. **Image Generation Phase**: Use nanobanana API to generate images based on placeholders
4. **Final Phase**: Compile everything into a single markdown file, then convert to PDF

### Key Components

- **Draft Structure**: One markdown file per chapter in a draft folder
- **Image Placeholders**: Format `![description](generated-filename.png)`
- **Image Storage**: Generated images saved to `img/` folder
- **Final Output**: Single consolidated markdown file converted to PDF

## File Structure

```
├── objectives.md              # Project specifications (Japanese)
├── sampleNanobananaAPIrequest.md  # API usage examples
├── .env                      # API keys (nanobanana API)
├── img/                      # Generated images (created during process)
├── draft/                    # Draft chapters (created during process)
└── final/                    # Final compiled book (created during process)
```

## API Integration

- **Image Generation**: Google nanobanana API
- **Authentication**: API key stored in `.env` file
- **Reference**: See `sampleNanobananaAPIrequest.md` for API usage patterns

## Development Notes

- All documentation is in Japanese
- No source code exists yet - this is a planning/specification phase
- The workflow is designed to be automated but implementation is pending
- Image generation is a key dependency requiring proper API integration
- Final output should be publication-ready PDF format