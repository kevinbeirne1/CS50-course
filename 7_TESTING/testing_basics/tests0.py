from prime import is_prime


def test_prime(n, expected):
    if is_prime(n) != expected:
        print(f"ERROR on is_prime({n}), expected {expected}")

# test_prime(4, False)
# test_prime(5, True)
# test_prime(10, False)
# test_prime(25, False)
