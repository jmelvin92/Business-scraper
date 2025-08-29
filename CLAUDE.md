# Business Scraper Project Documentation

## Project Overview
A simple, personal-use tool to identify businesses that are listed online but do not have websites. This tool helps find potential web development clients by scanning business directories and validating website presence.

## Key Decisions from Initial Planning

### Purpose
- **Personal tool**, not a product
- Focus on simplicity over features
- Identify businesses without websites for outreach opportunities

### Technical Approach
- **Local web application** (Python + Flask)
- Runs on localhost:5000
- No hosting, deployment, or external infrastructure needed
- Browser-based interface for ease of use

### Data Sources (100% Free)
1. **Primary**: Yelp Fusion API (5,000 free calls/day)
2. **Secondary**: Web scraping public directories (Yellow Pages, etc.)
3. **Future**: Government business registries, OpenStreetMap
4. **Note**: Will start with free sources, only consider paid APIs if needed

### Core Functionality
- Search by: State, City, Radius (miles)
- Returns: Business name, phone, address
- Export: CSV download
- **No complex features** - keeping it minimal

## Git Workflow

### IMPORTANT: Branch Strategy
- **Development Branch**: ALL work happens here
- **Main Branch**: Always kept in working state
- Never commit directly to main
- Merge to main only when features are complete and tested

### Repository
- GitHub: https://github.com/jmelvin92/Business-scraper

### Workflow
```bash
# Always work on development
git checkout development

# Make changes
git add .
git commit -m "descriptive message"
git push origin development

# Only merge to main when stable
git checkout main
git merge development
git push origin main
```

## Implementation Plan

### Phase 1: Basic Setup
1. Initialize Python project with virtual environment
2. Create Flask application structure
3. Set up development branch
4. Create basic HTML interface

### Phase 2: Core Functionality
1. Implement Yelp API integration
2. Add website validation logic
3. Create search functionality
4. Add CSV export

### Phase 3: Enhancement (if needed)
1. Add web scraping fallback
2. Implement caching to reduce API calls
3. Add basic error handling

## Project Structure
```
Business-scraper/
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # Simple search interface
├── static/
│   └── style.css       # Basic styling
├── scraper/
│   ├── yelp_api.py     # Yelp API integration
│   ├── validator.py    # Website validation
│   └── exporter.py     # CSV export
├── requirements.txt    # Python dependencies
├── .env               # API keys (not committed)
├── .gitignore
└── README.md
```

## Testing Commands
```bash
# Run the application
python app.py

# Run any tests (if implemented)
python -m pytest

# Lint checking (if configured)
python -m flake8
```

## Notes for Claude
- Keep code simple and readable
- Avoid over-engineering
- Focus on getting a working MVP first
- Always work on development branch
- Test locally before committing
- Document any API keys needed in .env.example

## Current Status
- Project initialized
- Planning complete
- Ready to begin implementation on development branch