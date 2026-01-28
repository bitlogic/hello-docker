#!/usr/bin/env python3
"""
Tests para el verificador del Último Teorema de Fermat.
"""

import pytest
from fermat_verifier import FermatVerifier


class TestFermatVerifier:
    """Tests para la clase FermatVerifier."""
    
    def test_pythagorean_triples_basic(self):
        """Verifica que se encuentren las tripletas Pitagóricas básicas."""
        verifier = FermatVerifier(max_value=30)
        triples = verifier.verify_pythagorean_triples()
        
        # Verificar que se encuentran las triples clásicas
        assert (3, 4, 5) in triples
        assert (5, 12, 13) in triples
        assert (8, 15, 17) in triples
    
    def test_no_solutions_for_n3(self):
        """Verifica que no hay soluciones para n=3."""
        verifier = FermatVerifier(max_value=50)
        solution = verifier.search_for_solutions(n=3, max_search=50)
        
        assert solution is None, "No debería haber soluciones para n=3"
    
    def test_no_solutions_for_n4(self):
        """Verifica que no hay soluciones para n=4."""
        verifier = FermatVerifier(max_value=50)
        solution = verifier.search_for_solutions(n=4, max_search=50)
        
        assert solution is None, "No debería haber soluciones para n=4"
    
    def test_no_solutions_for_n5(self):
        """Verifica que no hay soluciones para n=5."""
        verifier = FermatVerifier(max_value=50)
        solution = verifier.search_for_solutions(n=5, max_search=50)
        
        assert solution is None, "No debería haber soluciones para n=5"
    
    def test_range_verification(self):
        """Verifica múltiples exponentes."""
        verifier = FermatVerifier(max_value=30)
        results = verifier.verify_fermat_range(3, 6)
        
        # Para n >= 3, no debería haber soluciones
        for n in range(3, 7):
            assert results[n]['solution'] is None, f"No debería haber soluciones para n={n}"
    
    def test_pythagorean_triple_count(self):
        """Verifica el número de tripletas Pitagóricas."""
        verifier = FermatVerifier(max_value=100)
        triples = verifier.verify_pythagorean_triples()
        
        # Debería haber exactamente 52 tripletas para max_value=100
        assert len(triples) == 52, f"Se esperaban 52 tripletas, se encontraron {len(triples)}"
    
    def test_verifier_initialization(self):
        """Verifica la inicialización correcta del verificador."""
        verifier = FermatVerifier(max_value=150)
        
        assert verifier.max_value == 150
        assert isinstance(verifier.solutions_found, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
