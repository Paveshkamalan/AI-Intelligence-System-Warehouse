"""
Warehouse Safety Zone Module

Independent zone-management module.
Works with YOLO + ByteTrack coordinates.

Coordinate system:
1280 x 720
Origin = top-left
"""

import cv2
import numpy as np


# ============================================================
# WAREHOUSE ZONES
# ============================================================

ZONES = {

    "Loading Bay": np.array([
        [320, 180],
        [960, 180],
        [1080, 700],
        [200, 700]
    ], dtype=np.int32),

    "Worker Operating Area": np.array([
        [150, 350],
        [850, 350],
        [1200, 720],
        [50, 720]
    ], dtype=np.int32),

    "Storage Zone": np.array([
        [20, 20],
        [480, 20],
        [480, 380],
        [20, 380]
    ], dtype=np.int32),

    "Vehicle Zone": np.array([
        [0, 0],
        [520, 0],
        [520, 300],
        [0, 300]
    ], dtype=np.int32),

    "Wet Hazard Zone": np.array([
        [820, 520],
        [1270, 520],
        [1270, 720],
        [820, 720]
    ], dtype=np.int32),

    "Walkway": np.array([
        [920, 150],
        [1280, 150],
        [1280, 480],
        [920, 480]
    ], dtype=np.int32)
}


# ============================================================
# ZONE RISK LEVELS
# ============================================================

ZONE_RISK = {

    "Loading Bay": "HIGH",

    "Worker Operating Area": "MEDIUM",

    "Storage Zone": "MEDIUM",

    "Vehicle Zone": "CRITICAL",

    "Wet Hazard Zone": "HIGH",

    "Walkway": "LOW",

    "Unknown": "UNKNOWN"
}


# ============================================================
# ZONE PRIORITY
# ============================================================
#
# When zones overlap, the more safety-critical zone gets
# priority.
#
# Lower number = higher priority.
#

ZONE_PRIORITY = {

    "Vehicle Zone": 1,

    "Wet Hazard Zone": 2,

    "Loading Bay": 3,

    "Storage Zone": 4,

    "Worker Operating Area": 5,

    "Walkway": 6
}


# ============================================================
# GET ZONE
# ============================================================

def get_zone(point: tuple) -> str:

    """
    Determine the most important zone containing a point.

    Parameters
    ----------
    point : tuple
        (x, y) image coordinate.

    Returns
    -------
    str
        Zone name or "Unknown".
    """

    x, y = point

    matching_zones = []

    for zone_name, polygon in ZONES.items():

        result = cv2.pointPolygonTest(
            polygon,
            (float(x), float(y)),
            False
        )

        if result >= 0:
            matching_zones.append(zone_name)

    if not matching_zones:
        return "Unknown"

    # Select highest-priority zone
    matching_zones.sort(
        key=lambda zone: ZONE_PRIORITY[zone]
    )

    return matching_zones[0]


# ============================================================
# CHECK SPECIFIC ZONE
# ============================================================

def is_inside_zone(point: tuple, zone_name: str) -> bool:

    """
    Check whether a point is inside a specific zone.
    """

    if zone_name not in ZONES:
        return False

    x, y = point

    result = cv2.pointPolygonTest(
        ZONES[zone_name],
        (float(x), float(y)),
        False
    )

    return result >= 0


# ============================================================
# GET ALL MATCHING ZONES
# ============================================================

def get_all_zones(point: tuple) -> list:

    """
    Return every zone containing the point.

    Useful for debugging overlapping zones.
    """

    x, y = point

    matching_zones = []

    for zone_name, polygon in ZONES.items():

        result = cv2.pointPolygonTest(
            polygon,
            (float(x), float(y)),
            False
        )

        if result >= 0:
            matching_zones.append(zone_name)

    return matching_zones


# ============================================================
# GET RISK LEVEL
# ============================================================

def get_zone_risk(zone_name: str) -> str:

    """
    Return risk level associated with a zone.
    """

    return ZONE_RISK.get(
        zone_name,
        "UNKNOWN"
    )


# ============================================================
# DRAW ZONES
# ============================================================

def draw_zones(
    frame: np.ndarray,
    alpha: float = 0.25
) -> np.ndarray:

    """
    Draw warehouse zones on a video frame.
    """

    overlay = frame.copy()

    colors = {

        "Loading Bay":
            (0, 165, 255),

        "Worker Operating Area":
            (0, 255, 0),

        "Storage Zone":
            (255, 255, 0),

        "Vehicle Zone":
            (0, 0, 255),

        "Wet Hazard Zone":
            (255, 0, 255),

        "Walkway":
            (255, 255, 255)
    }

    for zone_name, polygon in ZONES.items():

        color = colors.get(
            zone_name,
            (200, 200, 200)
        )

        # Transparent fill
        cv2.fillPoly(
            overlay,
            [polygon],
            color
        )

        # Boundary
        cv2.polylines(
            frame,
            [polygon],
            True,
            color,
            2
        )

        # Label
        x, y = polygon[0]

        cv2.putText(
            frame,
            zone_name,
            (int(x), max(20, int(y) - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2,
            cv2.LINE_AA
        )

    # Blend
    cv2.addWeighted(
        overlay,
        alpha,
        frame,
        1 - alpha,
        0,
        frame
    )

    return frame