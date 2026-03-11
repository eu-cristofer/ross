"""Step 02: Build a healthy Sinha-like rotor model."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sinha_common import build_healthy_rotor, ensure_output_dir


def main():
    """Assemble model with initial equivalent supports and save it."""
    out_dir = ensure_output_dir()

    # Initial equivalent support guess before calibration.
    kxx0 = 2.0e6
    cxx0 = 50.0
    rotor, node_map = build_healthy_rotor(kxx=kxx0, cxx=cxx0)

    rotor_file = out_dir / "step_02_healthy_rotor_initial.toml"
    rotor.save(rotor_file)

    payload = {"kxx_initial_n_m": kxx0, "cxx_initial_n_s_m": cxx0, "node_map": node_map}
    metadata_file = out_dir / "step_02_model_metadata.json"
    metadata_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"Saved: {rotor_file}")
    print(f"Saved: {metadata_file}")


if __name__ == "__main__":
    main()
