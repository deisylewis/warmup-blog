# CSV Download and OpenAI Processing Application

This application automatically downloads CSV files from RB2B and HeyReach APIs, then processes them using OpenAI for analysis and insights.

## Features

- **Automated CSV Downloads**: Download CSV exports from RB2B and HeyReach APIs
- **OpenAI Processing**: Analyze CSV data using GPT-4 for insights, summaries, and custom analysis
- **Multiple Analysis Types**: Built-in analysis modes for insights, summaries, comparisons, and custom prompts
- **Scheduling**: Automated execution with flexible scheduling options
- **Comprehensive Logging**: Full logging of all operations with timestamps
- **Error Handling**: Robust error handling and validation
- **Flexible Configuration**: Environment-based configuration with sensible defaults

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the Application**:
   ```bash
   # Download CSVs and analyze with default insights
   python main.py
   
   # Download from specific source only
   python main.py --sources rb2b
   
   # Use custom OpenAI prompt
   python main.py --analysis-type custom --prompt "Analyze this data for marketing opportunities"
   ```

## Configuration

### Environment Variables

Create a `.env` file with your API credentials:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (at least one CSV source is recommended)
RB2B_API_KEY=your_rb2b_api_key_here
RB2B_API_URL=https://api.rb2b.com/v1/exports
HEYREACH_API_KEY=your_heyreach_api_key_here
HEYREACH_API_URL=https://api.heyreach.io/v1/exports

# Optional settings
DOWNLOAD_DIR=./downloads
PROCESSED_DIR=./processed
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000
```

## Usage Examples

### Basic Usage

```bash
# Download and analyze with default insights
python main.py

# Download only (skip OpenAI processing)
python main.py --download-only

# Process existing CSV files
python main.py --process-existing ./my-csv-folder
```

### Analysis Types

```bash
# Generate insights (default)
python main.py --analysis-type insights

# Generate executive summary
python main.py --analysis-type summary

# Compare multiple CSV files
python main.py --analysis-type compare

# Custom analysis with your own prompt
python main.py --analysis-type custom --prompt "Find the top 10 leads by engagement score"
```

### Source Selection

```bash
# Download from both sources (default)
python main.py --sources rb2b heyreach

# Download from RB2B only
python main.py --sources rb2b

# Download from HeyReach only
python main.py --sources heyreach
```

## Scheduling

Use the scheduler for automated execution:

```bash
# Run daily at 9 AM
python scheduler.py --schedule-type daily --time 09:00

# Run every hour
python scheduler.py --schedule-type hourly

# Run every 30 minutes
python scheduler.py --schedule-type interval --interval 30

# Run once immediately, then start daily schedule
python scheduler.py --schedule-type daily --run-now
```

## File Structure

```
.
├── main.py              # Main application entry point
├── csv_downloader.py    # CSV download functionality
├── openai_processor.py  # OpenAI processing functionality
├── scheduler.py         # Automated scheduling
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── downloads/          # Downloaded CSV files (created automatically)
├── processed/          # OpenAI analysis results (created automatically)
└── *.log              # Application log files
```

## Analysis Output

The application generates several types of output:

### CSV Download Results
- Downloaded CSV files with timestamps
- Validation reports
- Download logs

### OpenAI Analysis Results
- JSON files with complete analysis results
- Processing metadata (tokens used, model, timestamp)
- Pipeline summaries

### Example Output Structure
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "source_csv": "./downloads/rb2b_export_20240115_103000.csv",
  "prompt": "Analyze this data for insights...",
  "csv_info": {
    "rows": 1250,
    "columns": ["name", "email", "company", "score"],
    "file_size": 245760
  },
  "openai_response": "Analysis results here...",
  "model_used": "gpt-4",
  "tokens_used": 1847
}
```

## API Integration

### RB2B API
The application expects RB2B to provide CSV exports via their API endpoint. Configure the endpoint URL and authentication in your `.env` file.

### HeyReach API
Similar to RB2B, configure HeyReach API credentials and endpoint for CSV exports.

### OpenAI API
Uses OpenAI's Chat Completions API with GPT-4 for data analysis. Supports custom prompts and various analysis types.

## Error Handling

The application includes comprehensive error handling:
- API connection failures
- Invalid CSV data
- OpenAI API errors
- File system issues
- Authentication problems

All errors are logged with timestamps and context for debugging.

## Logging

Multiple log files are created:
- `app.log`: Main application logs
- `csv_downloader.log`: Download-specific logs
- `scheduler.log`: Scheduler operation logs

## Development

### Adding New CSV Sources
1. Extend the `CSVDownloader` class
2. Add new download method following the existing pattern
3. Update the main application to include the new source

### Custom Analysis Types
1. Add new methods to `OpenAIProcessor` class
2. Update the main application argument parser
3. Add appropriate validation logic

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure all required API keys are set in `.env`
2. **Download Failures**: Check API endpoints and network connectivity
3. **OpenAI Errors**: Verify OpenAI API key and check token limits
4. **File Permissions**: Ensure write permissions for download and processed directories

### Debug Mode
Enable debug logging by setting the logging level to DEBUG in the respective modules.

## License

This project is open source. Please ensure you comply with the terms of service for all integrated APIs (OpenAI, RB2B, HeyReach).