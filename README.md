# Gyrocompass Overhaul Checklist Application

A professional GUI-based checklist management system for gyrocompass maintenance and overhaul procedures, with automatic PDF report generation.

## Features

- **Interactive GUI**: User-friendly interface with tabbed categories
- **Comprehensive Checklist**: 6 categories with 45+ maintenance items:
  - Initial Inspection
  - Mechanical Inspection
  - Electrical Testing
  - Functional Testing
  - Alignment & Calibration
  - Documentation & Cleanup
- **Data Persistence**: Save and load checklist data in JSON format
- **PDF Reports**: Generate professional reports with:
  - Technician and equipment information
  - Complete checklist status
  - Completion summary and statistics
  - Signature lines for sign-off
- **Notes & Comments**: Add notes to individual items
- **Progress Tracking**: Track completion percentage

## Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- reportlab (for PDF generation)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mkspogon123/gyrocompass-overhaul-checklist.git
cd gyrocompass-overhaul-checklist
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python main.py
```

### Basic Workflow

1. **Enter Information**:
   - Enter your name as technician
   - Enter the equipment ID
   - Set the start date (defaults to today)

2. **Complete Checklist**:
   - Navigate through different categories using tabs
   - Check off items as you complete them
   - Add notes to each item for additional context (optional)

3. **Save Your Progress**:
   - Click "Save Checklist" to save progress in JSON format
   - You can load this later to continue work

4. **Generate Report**:
   - Click "Generate Report" to create a PDF
   - Select where to save the PDF file
   - Report includes all checklist items, completion status, and sign-off area

5. **Additional Options**:
   - "Load Checklist" - Resume from a previous save
   - "Reset All" - Clear all checkmarks and notes
   - "Exit" - Close the application

## File Structure

```
gyrocompass-overhaul-checklist/
├── main.py                 # Main application GUI
├── checklist_data.py       # Checklist categories and items
├── report_generator.py     # PDF report generation
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Checklist Categories

### Initial Inspection (6 items)
Visual inspection, damage check, hardware verification, connector inspection, documentation, serial number verification

### Mechanical Inspection (8 items)
Rotor inspection, bearing check, gimbal suspension, follow-up system, erection mechanism, damping system, lubrication

### Electrical Testing (8 items)
Power supply, current draw, heating element, motor function, servo motor, amplifier circuits, signal conditioning, repeater connections

### Functional Testing (8 items)
Spin-up test, spin-up time monitoring, vibration check, precession verification, settling time test, heading lock, rate of turn, heading repeatability

### Alignment & Calibration (7 items)
Gyro leveling, meridian transit accuracy, compass azimuth calibration, latitude correction, repeater synchronization, earth rate compensation, heading output calibration

### Documentation & Cleanup (8 items)
Test results documentation, replacement records, lubrication notes, cleaning, cover reinstallation, connection verification, maintenance log update, completion sign-off

## PDF Report Output

The generated PDF includes:
- Header information (technician, equipment ID, dates)
- Detailed checklist organized by category
- Completion status (✓ or ○) for each item
- Item-specific notes
- Summary statistics:
  - Total items in checklist
  - Number of completed items
  - Number of incomplete items
  - Overall completion percentage
- Sign-off section for technician and supervisor

## Data Format (JSON)

Checklists are saved in JSON format for easy sharing and archival:

```json
{
  "technician": "John Smith",
  "equipment_id": "GC-001",
  "start_date": "2024-01-15",
  "completion_date": "2024-01-15 14:30:00",
  "categories": {
    "Initial Inspection": [
      {
        "name": "Visual inspection of external casing",
        "completed": true,
        "notes": "No visible damage found"
      }
    ]
  }
}
```

## Customization

To add or modify checklist items, edit `checklist_data.py`:

```python
CHECKLIST_CATEGORIES = {
    "Your Category": [
        "Item 1",
        "Item 2",
        # Add more items
    ]
}
```

## Troubleshooting

### "reportlab not installed" Error
```bash
pip install reportlab
```

### GUI not appearing
Ensure tkinter is installed:
- **Windows**: Usually included with Python
- **macOS**: Usually included with Python
- **Linux**: `sudo apt-get install python3-tk`

### PDF generation fails
- Ensure you have write permissions in the selected directory
- Check that the file path doesn't contain invalid characters

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.7+
- **Memory**: Minimal (< 50 MB)
- **Disk**: Minimal, PDFs vary by report detail

## License

MIT License - Feel free to use and modify for your needs

## Support & Feedback

For issues, suggestions, or improvements, feel free to modify and adapt this application to your specific needs.

## Disclaimer

This application is designed for gyrocompass maintenance tracking. Always refer to manufacturer documentation and follow proper maintenance procedures. Ensure all work is performed by qualified technicians following appropriate safety protocols.