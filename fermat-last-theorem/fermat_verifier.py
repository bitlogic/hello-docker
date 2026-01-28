#!/usr/bin/env python3
"""
Último Teorema de Fermat - Verificador Computacional

Este programa verifica computacionalmente que no existen soluciones enteras
positivas a la ecuación x^n + y^n = z^n para n > 2 en un rango limitado.

NOTA: Esto NO es una demostración matemática del teorema. Es simplemente
una verificación empírica para valores pequeños con fines educativos.
"""

import sys
import time
from typing import List, Tuple, Optional


class FermatVerifier:
    """Verificador del Último Teorema de Fermat para valores pequeños."""
    
    def __init__(self, max_value: int = 100):
        """
        Inicializa el verificador.
        
        Args:
            max_value: Valor máximo para x, y, z a verificar
        """
        self.max_value = max_value
        self.solutions_found = {}
    
    def verify_pythagorean_triples(self) -> List[Tuple[int, int, int]]:
        """
        Encuentra tripletas Pitagóricas (n=2) como casos conocidos.
        
        Returns:
            Lista de tripletas (x, y, z) donde x² + y² = z²
        """
        triples = []
        for x in range(1, self.max_value):
            for y in range(x, self.max_value):
                z_squared = x*x + y*y
                z = int(z_squared ** 0.5)
                if z <= self.max_value and z*z == z_squared:
                    triples.append((x, y, z))
        return triples
    
    def search_for_solutions(self, n: int, max_search: int = None) -> Optional[Tuple[int, int, int]]:
        """
        Busca soluciones para x^n + y^n = z^n.
        
        Args:
            n: El exponente a verificar
            max_search: Límite máximo de búsqueda (usa self.max_value si es None)
            
        Returns:
            Tupla (x, y, z) si se encuentra una solución, None en caso contrario
        """
        if max_search is None:
            max_search = self.max_value
            
        for x in range(1, max_search):
            for y in range(x, max_search):
                # Calcular z^n = x^n + y^n
                sum_powers = x**n + y**n
                
                # Estimación de z
                z = int(sum_powers ** (1/n))
                
                # Verificar z y z+1 por errores de redondeo
                for z_candidate in [z, z + 1]:
                    if z_candidate <= max_search and z_candidate**n == sum_powers:
                        return (x, y, z_candidate)
        
        return None
    
    def verify_fermat_range(self, n_start: int, n_end: int) -> dict:
        """
        Verifica el teorema para un rango de exponentes.
        
        Args:
            n_start: Exponente inicial
            n_end: Exponente final (inclusive)
            
        Returns:
            Diccionario con resultados para cada n
        """
        results = {}
        
        for n in range(n_start, n_end + 1):
            print(f"\n{'='*60}")
            print(f"Verificando n = {n}")
            print(f"{'='*60}")
            
            start_time = time.time()
            solution = self.search_for_solutions(n)
            elapsed = time.time() - start_time
            
            if solution:
                x, y, z = solution
                print(f"⚠️  ¡SOLUCIÓN ENCONTRADA! {x}^{n} + {y}^{n} = {z}^{n}")
                print(f"   Verificación: {x**n} + {y**n} = {z**n}")
                results[n] = {'solution': solution, 'time': elapsed}
            else:
                print(f"✓ No se encontraron soluciones para n={n}")
                print(f"  Rango verificado: 1 ≤ x,y,z ≤ {self.max_value}")
                print(f"  Tiempo: {elapsed:.3f} segundos")
                results[n] = {'solution': None, 'time': elapsed}
        
        return results
    
    def demonstrate_theorem(self):
        """Ejecuta una demostración completa del teorema."""
        print("\n" + "="*60)
        print("ÚLTIMO TEOREMA DE FERMAT - Verificación Computacional")
        print("="*60)
        print(f"\nTeorema: No existen enteros positivos x, y, z tales que:")
        print(f"         x^n + y^n = z^n  para n > 2")
        print(f"\nRango de verificación: 1 ≤ x,y,z ≤ {self.max_value}")
        print("="*60)
        
        # Caso n=1 (trivial)
        print("\n" + "-"*60)
        print("CASO n = 1 (Trivial - Suma ordinaria)")
        print("-"*60)
        print("Ejemplo: 2 + 3 = 5")
        print("Existen infinitas soluciones para n=1")
        
        # Caso n=2 (Tripletas Pitagóricas)
        print("\n" + "-"*60)
        print("CASO n = 2 (Tripletas Pitagóricas)")
        print("-"*60)
        triples = self.verify_pythagorean_triples()
        print(f"Se encontraron {len(triples)} tripletas Pitagóricas:")
        for i, (x, y, z) in enumerate(triples[:10], 1):
            print(f"  {i}. {x}² + {y}² = {z}²  →  {x**2} + {y**2} = {z**2}")
        if len(triples) > 10:
            print(f"  ... y {len(triples) - 10} más")
        
        # Casos n > 2 (El Teorema de Fermat)
        print("\n" + "-"*60)
        print("CASOS n > 2 (Último Teorema de Fermat)")
        print("-"*60)
        results = self.verify_fermat_range(3, 10)
        
        # Resumen
        print("\n" + "="*60)
        print("RESUMEN")
        print("="*60)
        print(f"• n = 1: Infinitas soluciones (suma trivial)")
        print(f"• n = 2: {len(triples)} tripletas Pitagóricas encontradas")
        
        solutions_found = False
        for n in range(3, 11):
            if results[n]['solution']:
                solutions_found = True
                x, y, z = results[n]['solution']
                print(f"• n = {n}: ¡SOLUCIÓN! {x}^{n} + {y}^{n} = {z}^{n}")
        
        if not solutions_found:
            print(f"• n ≥ 3: NO se encontraron soluciones (consistente con el teorema)")
        
        print("\n" + "="*60)
        print("CONCLUSIÓN")
        print("="*60)
        print(f"Para todos los valores verificados (n = 3 a 10, rango 1-{self.max_value}):")
        print("NO existen soluciones enteras a x^n + y^n = z^n")
        print("\nEsto es consistente con el Último Teorema de Fermat.")
        print("\nNOTA: Esta verificación computacional NO constituye una")
        print("demostración matemática. La demostración real fue realizada")
        print("por Andrew Wiles en 1995 usando teoría avanzada de números.")
        print("="*60 + "\n")


def main():
    """Función principal."""
    # Configuración
    max_value = 100  # Límite de búsqueda
    
    # Permitir override desde línea de comandos
    if len(sys.argv) > 1:
        try:
            max_value = int(sys.argv[1])
        except ValueError:
            print(f"Error: '{sys.argv[1]}' no es un número válido")
            print(f"Uso: {sys.argv[0]} [max_value]")
            sys.exit(1)
    
    # Crear verificador y ejecutar
    verifier = FermatVerifier(max_value=max_value)
    verifier.demonstrate_theorem()


if __name__ == "__main__":
    main()
