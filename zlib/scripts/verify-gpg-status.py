import sys

expected_signer = sys.argv[1].replace(" ", "").upper()
expected_primary = sys.argv[2].replace(" ", "").upper()

with open(sys.argv[3], encoding="ascii") as f:
    valid = [
        line.split()
        for line in f
        if line.startswith("[GNUPG:] VALIDSIG ")
    ]

if len(valid) != 1:
    raise SystemExit(f"expected exactly one valid signature, got {len(valid)}")

fields = valid[0]
if len(fields) != 12:
    raise SystemExit("VALIDSIG did not include the primary-key fingerprint")

if fields[2].upper() != expected_signer:
    raise SystemExit(f"wrong signing key: {fields[2]}")
if fields[11].upper() != expected_primary:
    raise SystemExit(f"wrong primary key: {fields[11]}")
