# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a book creation system that generates books from given instructions and information. The project follows a four-phase workflow: draft creation, draft review, image generation using Google Gemini API, and final book compilation with PDF conversion.

**Status**: Fully implemented and tested (2025-10-17)

## Architecture and Workflow

The system follows this processing flow:

1. **Input Phase**: Receive instructions and information, validate completeness
2. **Draft Phase**: Create structure proposal, generate markdown files per chapter with image placeholders
3. **Review Phase**: Technical review of draft content for accuracy (especially scientific/safety information)
4. **Image Generation Phase**: Use Google Gemini API (gemini-2.5-flash-image-preview) to generate images
5. **Finalization Phase**:
   - Compile all chapters into single markdown file
   - Generate print-ready HTML with CSS styling
   - Convert to PDF using Chrome headless mode

### Key Components

- **Draft Structure**: One markdown file per chapter in a draft folder
- **Image Placeholders**: Format `![description](generated-filename.png)`
- **Image Storage**: Generated images saved to `img/` folder
- **Final Output**: Single consolidated markdown file converted to PDF

## File Structure

```
├── objectives.md              # Project specifications (Japanese)
├── sampleGeminiImageAPI.md    # Gemini API usage examples (renamed from nanobanana)
├── .env                       # API keys (Gemini API)
├── .env.example               # API key template
├── generate_images.py         # Main image generation script (v2.0)
├── test_generate_10.py        # Test script for first 10 images
├── create_print_ready_html.py # HTML generation for PDF conversion
├── img/                       # Generated images (created during process)
├── draft/                     # Draft chapters (created during process)
└── final/                     # Final compiled book (created during process)
    ├── *.md                   # Consolidated markdown
    ├── *_印刷用.html          # Print-ready HTML
    └── *.pdf                  # Final PDF output
```

## API Integration

### Image Generation
- **API**: Google Gemini API
- **Model**: `gemini-2.5-flash-image-preview`
- **Authentication**: API key stored in `.env` file (requires paid plan for bulk generation)
- **Quota**: Free tier insufficient for book projects; paid plan recommended
- **Rate Limiting**: 1.5 second delay between requests recommended
- **Reference**: See `sampleGeminiImageAPI.md` for API usage patterns

### API Response Handling
The Gemini API response structure requires robust parsing:
- Response may contain multiple parts (text + image)
- Image data location varies (not always in parts[0])
- Data format varies (bytes or base64-encoded string)
- See implementation in `generate_images.py` for production-ready code

### Cost Estimation
- Standard requests: ~$0.039 per image
- Batch API: Not supported for image generation models
- Estimated cost for 160 images: $6-7 USD

## Implementation Notes

### Completed Components
- ✅ Draft generation workflow
- ✅ Image generation scripts with robust error handling
- ✅ PDF conversion pipeline (Markdown → HTML → PDF)
- ✅ Print-ready HTML generation with CSS styling

### Technical Stack
- **Python 3.9+**: Core scripting language
- **google-generativeai**: Gemini API client
- **Pillow**: Image processing
- **pandoc**: Markdown to HTML conversion
- **Google Chrome**: Headless PDF generation (best Japanese support)

### Known Limitations
- **PDF Generation**: Requires Chrome installation
  - Alternative tools (WeasyPrint, htmldoc) have issues with Japanese text
- **Image Generation Time**: ~30 minutes for 160 images (11 seconds/image average)
- **PDF File Size**: Large files (200MB+) due to embedded images

### Best Practices
1. Test with 10 images first (`test_generate_10.py`)
2. Check API quota before bulk generation
3. Use paid Gemini API plan for projects with 50+ images
4. Verify PDF rendering with sample before full generation

## Development Notes

- All documentation is in Japanese
- Image generation uses improved prompts with context and type-specific templates
- Final output should be publication-ready PDF format
