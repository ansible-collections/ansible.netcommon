"""
Test utilities for hashing expectations.

Background:
- ansible-core PR 85970 replaced passlib-based hashing (passlib_or_crypt)
  with the core's do_encrypt implementation for md5_crypt in 2.20+.
- This causes different formatting/behavior in some environments, breaking
  tests that hardcode the historical passlib output.

This helper normalizes expectations by selecting the backend based on
  the ansible-core version (not import availability):
  - core >= 2.20 -> ansible.utils.encrypt.do_encrypt
  - core <  2.20 -> ansible.utils.encrypt.passlib_or_crypt
If those imports unexpectedly fail, we fall back to stdlib crypt.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


def get_expected_md5_crypt(password, salt):
    """
    Return the expected md5_crypt hash for a given password and salt,
    based on the ansible-core in use.

    Preference order:
    1) ansible.utils.encrypt.do_encrypt (core >= 2.20)
    2) ansible.utils.encrypt.passlib_or_crypt (core < 2.20)
    3) stdlib crypt as a last resort
    """

    # Choose implementation based on ansible-core version
    try:
        from ansible import release as ansible_release

        version_str = getattr(ansible_release, "__version__", "0.0")

        def _cmp_version(ver, thresh_major, thresh_minor):
            parts = ver.split(".")
            try:
                major = int(parts[0]) if len(parts) > 0 else 0
            except ValueError:
                major = 0
            try:
                minor = int(parts[1]) if len(parts) > 1 else 0
            except ValueError:
                minor = 0
            return (major, minor) >= (thresh_major, thresh_minor)

        use_do_encrypt = _cmp_version(version_str, 2, 20)
    except ImportError:
        # If ansible is not importable, assume legacy behavior
        use_do_encrypt = False

    if use_do_encrypt:
        try:
            from ansible.utils.encrypt import do_encrypt

            return do_encrypt(password, "md5_crypt", salt=salt)
        except ImportError:
            # Unexpected for core >= 2.20; fall back to stdlib crypt
            try:
                import crypt

                return crypt.crypt(password, "$1$%s$" % salt)
            except Exception as crypt_exc:
                raise RuntimeError("No suitable hashing backend available for tests") from crypt_exc
    else:
        try:
            from ansible.utils.encrypt import passlib_or_crypt

            return passlib_or_crypt(password, "md5_crypt", salt=salt)
        except ImportError:
            # Fall back to stdlib crypt when passlib/crypt not available
            try:
                import crypt

                return crypt.crypt(password, "$1$%s$" % salt)
            except Exception as crypt_exc:
                raise RuntimeError("No suitable hashing backend available for tests") from crypt_exc
