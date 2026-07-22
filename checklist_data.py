"""
Gyrocompass overhaul checklist categories and items
"""

CHECKLIST_CATEGORIES = {
    "Initial Inspection": [
        "Visual inspection of external casing",
        "Check for physical damage or corrosion",
        "Verify mounting hardware integrity",
        "Inspect electrical connectors",
        "Document current condition with photos",
        "Check serial number and model number",
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
    ],
    "Alignment & Calibration": [
        "Perform gyro leveling",
        "Check meridian transit accuracy",
        "Calibrate compass azimuth",
        "Verify latitude correction settings",
        "Test course-up repeater synchronization",
        "Perform earth rate compensation check",
        "Calibrate heading output",
    ],
    "Documentation & Cleanup": [
        "Document all test results",
        "Record any replacements made",
        "Note lubrication points serviced",
        "Clean exterior surfaces",
        "Reinstall protective covers",
        "Verify all connections are secure",
        "Update maintenance log",
        "Sign off completion",
    ],
}

TEST_CRITERIA = {
    "Spin-up Time": "Should complete within 3-5 minutes",
    "Settling Time": "Should stabilize within 15 minutes",
    "Heading Accuracy": "±1° or better",
    "Repeatability": "Within 0.5° over 24 hours",
    "Response Time": "Less than 10 seconds to course change",
}