"""
Shared Warehouse Safety System State

Provides one shared SafetyIntelligence instance
for the video processor and FastAPI.
"""

from vision.safety.safety_intelligence import SafetyIntelligence


safety_intelligence = SafetyIntelligence()
