#!/usr/bin/env python3
"""
Tests simples para el verificador del Último Teorema de Fermat.
No requiere pytest - solo la biblioteca estándar.
"""

from fermat_verifier import FermatVerifier


def test_pythagorean_triples():
    """Verifica tripletas Pitagóricas."""
    print("Test: Tripletas Pitagóricas...")
    verifier = FermatVerifier(max_value=30)
    triples = verifier.verify_pythagorean_triples()
    
    assert (3, 4, 5) in triples, "Falta la tripleta (3, 4, 5)"
    assert (5, 12, 13) in triples, "Falta la tripleta (5, 12, 13)"
    assert (8, 15, 17) in triples, "Falta la tripleta (8, 15, 17)"
    print("  ✓ Tripletas Pitagóricas encontradas correctamente")


def test_no_solutions_n3():
    """Verifica que no hay soluciones para n=3."""
    print("Test: Sin soluciones para n=3...")
    verifier = FermatVerifier(max_value=50)
    solution = verifier.search_for_solutions(n=3, max_search=50)
    
    assert solution is None, "No debería haber soluciones para n=3"
    print("  ✓ No se encontraron soluciones para n=3 (correcto)")


def test_no_solutions_n4():
    """Verifica que no hay soluciones para n=4."""
    print("Test: Sin soluciones para n=4...")
    verifier = FermatVerifier(max_value=50)
    solution = verifier.search_for_solutions(n=4, max_search=50)
    
    assert solution is None, "No debería haber soluciones para n=4"
    print("  ✓ No se encontraron soluciones para n=4 (correcto)")


def test_no_solutions_n5():
    """Verifica que no hay soluciones para n=5."""
    print("Test: Sin soluciones para n=5...")
    verifier = FermatVerifier(max_value=50)
    solution = verifier.search_for_solutions(n=5, max_search=50)
    
    assert solution is None, "No debería haber soluciones para n=5"
    print("  ✓ No se encontraron soluciones para n=5 (correcto)")


def test_multiple_exponents():
    """Verifica múltiples exponentes."""
    print("Test: Múltiples exponentes (n=3 a n=6)...")
    verifier = FermatVerifier(max_value=30)
    results = verifier.verify_fermat_range(3, 6)
    
    for n in range(3, 7):
        assert results[n]['solution'] is None, f"No debería haber soluciones para n={n}"
    print("  ✓ No se encontraron soluciones para n=3..6 (correcto)")


def test_pythagorean_count():
    """Verifica el conteo de tripletas Pitagóricas."""
    print("Test: Conteo de tripletas Pitagóricas...")
    verifier = FermatVerifier(max_value=100)
    triples = verifier.verify_pythagorean_triples()
    
    assert len(triples) == 52, f"Se esperaban 52 tripletas, se encontraron {len(triples)}"
    print(f"  ✓ Se encontraron {len(triples)} tripletas Pitagóricas (correcto)")


def main():
    """Ejecuta todos los tests."""
    print("\n" + "="*60)
    print("EJECUTANDO TESTS DEL VERIFICADOR DE FERMAT")
    print("="*60 + "\n")
    
    tests = [
        test_pythagorean_triples,
        test_no_solutions_n3,
        test_no_solutions_n4,
        test_no_solutions_n5,
        test_multiple_exponents,
        test_pythagorean_count,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ FALLO: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTADOS: {passed} tests pasaron, {failed} tests fallaron")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
