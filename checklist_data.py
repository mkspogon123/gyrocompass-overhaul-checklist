"""
Gyrocompass overhaul checklist categories organized by model
"""

# Different gyrocompass models with their specific checklists
GYRO_MODELS = {
    "Yogkowaga CMZ700": {
        "manufacturer": "Yogkowaga",
        "type": "Electronic Gyrocompass",
        "description": "Yogkowaga CMZ700 Marine Gyrocompass"
    },
    "Yogkowaga CMZ900": {
        "manufacturer": "Yogkowaga",
        "type": "Electronic Gyrocompass",
        "description": "Yogkowaga CMZ900 Marine Gyrocompass"
    },
    "Anschütz STD22": {
        "manufacturer": "Anschütz",
        "type": "Electronic Gyrocompass",
        "description": "Anschütz STD22 Standard Gyrocompass"
    },
    "Simrad GC80/85": {
        "manufacturer": "Simrad",
        "type": "Electronic Gyrocompass",
        "description": "Simrad GC80/85 Integrated Gyrocompass"
    }
}

# Base checklist categories (same for all models)
CHECKLIST_CATEGORIES = {
    "Initial Inspection": [
        "Visual inspection of external casing",
        "Check for physical damage or corrosion",
        "Verify mounting hardware integrity",
        "Inspect electrical connectors",
        "Document current condition with photos",
        "Check serial number and model number",
        "Verify equipment documentation available",
    ],
    "Mechanical Inspection": [
        "Remove protective covers",
        "Inspect rotor assembly",
        "Check gyroscope bearings for wear",
        "Verify gimbal suspension integrity",
        "Inspect follow-up system",
        "Check erection mechanism",
        "Verify damping system components",
        "Lubricate bearings if required",
        "Check pendulum assembly (if applicable)",
    ],
    "Electrical Testing": [
        "Test power supply voltage",
        "Measure current draw",
        "Check heating element resistance",
        "Verify synchronous motor function",
        "Test servo motor operation",
        "Check amplifier circuits",
        "Verify signal conditioning circuits",
        "Test compass repeater connections",
        "Check resolver/synchro outputs",
    ],
    "Functional Testing": [
        "Spin up gyroscope (no load)",
        "Monitor spin-up time",
        "Check for vibration or noise",
        "Verify precession movement",
        "Test settling time after disturbance",
        "Verify heading lock function",
        "Test rate of turn response",
        "Check heading repeatability",
        "Verify north-seeking accuracy",
    ],
    "Alignment & Calibration": [
        "Perform gyro leveling",
        "Check meridian transit accuracy",
        "Calibrate compass azimuth",
        "Verify latitude correction settings",
        "Test course-up repeater synchronization",
        "Perform earth rate compensation check",
        "Calibrate heading output",
        "Verify gyro error within limits",
    ],
    "System Integration & Testing": [
        "Test NMEA 0183 output",
        "Verify autopilot integration",
        "Test chart plotter interface",
        "Check multi-unit synchronization (if applicable)",
        "Verify backup power operation",
        "Test alarm/warning systems",
        "Verify display screen functionality",
        "Document all test readings",
    ],
    "Documentation & Cleanup": [
        "Document all test results",
        "Record any replacements made",
        "Note lubrication points serviced",
        "Clean exterior surfaces",
        "Reinstall protective covers",
        "Verify all connections are secure",
        "Update maintenance log",
        "Complete maintenance record",
        "Sign off completion",
    ],
}

# Standard test acceptance criteria
TEST_CRITERIA = {
    "Spin-up Time": "Should complete within 3-5 minutes",
    "Settling Time": "Should stabilize within 15 minutes",
    "Heading Accuracy": "±1° or better",
    "Repeatability": "Within 0.5° over 24 hours",
    "Response Time": "Less than 10 seconds to course change",
    "Gyro Error": "Less than ±2° per hour",
}

# Model-specific notes
MODEL_NOTES = {
    "Yogkowaga CMZ700": "Entry-level electronic compass - Check heating elements and servo calibration carefully",
    "Yogkowaga CMZ900": "Advanced electronic compass - Verify dual-channel redundancy and cross-track monitoring",
    "Anschütz STD22": "Compact design - Limited access to internals, check resolver alignment precision",
    "Simrad GC80/85": "Integrated ECDIS system - NMEA output and network integration critical",
}
