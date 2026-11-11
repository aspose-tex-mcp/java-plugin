"""Source-checkout launcher; installed deployments use adcs_tex_java.worker."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from adcs_tex_java.worker import main

if __name__ == "__main__":
    main()
