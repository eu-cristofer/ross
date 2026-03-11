"""Step 01: Define Sinha rig geometry and check units."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ross.units import Q_

from sinha_common import ensure_output_dir, rig_spec


def main():
    """Write assumptions and unit checks for the workflow."""
    out_dir = ensure_output_dir()
    spec = rig_spec()

    checks = {
        "shaft_length_mm": Q_(spec["shaft_length_m"], "m").to("mm").m,
        "shaft_od_mm": Q_(spec["shaft_od_m"], "m").to("mm").m,
        "bearing_left_mm": Q_(spec["bearing_left_x_m"], "m").to("mm").m,
        "bearing_right_mm": Q_(spec["bearing_right_x_m"], "m").to("mm").m,
        "disk_center_mm": Q_(spec["disk_x_m"], "m").to("mm").m,
        "target_f1_rad_s": Q_(spec["target_f1_hz"], "Hz").to("rad/s").m,
    }

    payload = {
        "description": "Sinha 2007 rig assumptions and conversions",
        "spec_si": spec,
        "unit_checks": checks,
    }

    output_file = out_dir / "step_01_assumptions.json"
    output_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Saved: {output_file}")


if __name__ == "__main__":
    main()
