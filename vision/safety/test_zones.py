from zones import (
    get_zone,
    get_all_zones,
    get_zone_risk
)


test_points = [

    (100, 100),

    (400, 200),

    (300, 500),

    (1000, 600),

    (1000, 300),

    (600, 100)
]


print("================================")
print("ZONE TEST")
print("================================")

for point in test_points:

    zone = get_zone(point)

    all_zones = get_all_zones(point)

    risk = get_zone_risk(zone)

    print()
    print(f"Point: {point}")
    print(f"Primary Zone: {zone}")
    print(f"All Zones: {all_zones}")
    print(f"Risk: {risk}")

print()
print("================================")