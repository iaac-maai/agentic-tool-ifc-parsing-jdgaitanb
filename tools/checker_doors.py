"""
IFC Compliance Checker - Door accessibility example.

This module implements a simple compliance check that verifies
doors meet a minimum width requirement.
"""

import ifcopenshell


def check_door_accessibility(model, min_width_mm: float = 900.0, **kwargs) -> list[dict]:
    """
    Check that all doors have at least the given minimum width.

    Width is taken from IfcDoor.OverallWidth if available.
    """
    results: list[dict] = []

    doors = model.by_type("IfcDoor") if hasattr(model, "by_type") else []

    compliant_count = 0
    non_compliant_count = 0

    for door in doors:
        width = getattr(door, "OverallWidth", None)
        has_width = width is not None

        if has_width and width >= min_width_mm:
            status = "pass"
            compliant_count += 1
            comment = None
        else:
            # Either missing width or below requirement
            status = "fail"
            non_compliant_count += 1
            if not has_width:
                comment = "Door width is not specified (OverallWidth is missing)"
            else:
                comment = (
                    f"Door width {width} mm is below required minimum {min_width_mm} mm"
                )

        results.append(
            {
                "element_id": getattr(door, "GlobalId", None),
                "element_type": "IfcDoor",
                "element_name": getattr(door, "Name", None) or f"Door #{door.id()}",
                "element_name_long": None,
                "check_status": status,
                "actual_value": str(width) if has_width else "Unknown width",
                "required_value": f">= {min_width_mm} mm",
                "comment": comment,
                "log": None,
            }
        )

    total_doors = len(doors)

    if total_doors == 0:
        summary_status = "warning"
        summary_comment = "Model contains no IfcDoor elements"
    elif non_compliant_count == 0:
        summary_status = "pass"
        summary_comment = f"All {total_doors} doors meet or exceed the minimum width"
    else:
        summary_status = "fail"
        summary_comment = (
            f"{non_compliant_count} of {total_doors} doors are below the "
            f"required minimum width of {min_width_mm} mm or have no width set"
        )

    results.append(
        {
            "element_id": None,
            "element_type": "Summary",
            "element_name": "Door Accessibility Check",
            "element_name_long": None,
            "check_status": summary_status,
            "actual_value": f"{compliant_count} / {total_doors} doors compliant",
            "required_value": f"All doors width >= {min_width_mm} mm",
            "comment": summary_comment,
            "log": None,
        }
    )

    return results


if __name__ == "__main__":
    # Ejecutar la batería de tests al darle "Run" en Cursor,
    # para que puedas ver que pasan los 13 tests de la entrega.
    import pytest
    import sys

    print("Lanzando tests de la entrega con pytest...\n")
    exit_code = pytest.main([])
    print("\nFin de pytest (exit code:", exit_code, ")")
    sys.exit(exit_code)
