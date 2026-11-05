import unittest
from pathlib import Path


class PatchCleanlinessTests(unittest.TestCase):
    def test_patches_contain_no_nul_bytes(self):
        """A NUL byte inside a patch lands verbatim in the generated Swift
        source, where the compiler rejects it with 'nul character embedded
        in middle of file'. This once shipped inside string literals that
        lost their emoji to a byte-level rename, so guard every patch."""
        patches_dir = Path(__file__).resolve().parent.parent.parent / "patches"
        offenders = []
        for patch in sorted(patches_dir.glob("*.patch")):
            if b"\x00" in patch.read_bytes():
                offenders.append(patch.name)
        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
