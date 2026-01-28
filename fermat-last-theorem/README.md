# Último Teorema de Fermat

## Contexto Histórico

El **Último Teorema de Fermat** fue enunciado por Pierre de Fermat en 1637 en el margen de su copia de la *Aritmética* de Diofanto. Fermat escribió que había descubierto una demostración maravillosa, pero que el margen era demasiado pequeño para contenerla.

## El Teorema

**Enunciado:** No existen números enteros positivos x, y, z que satisfagan la ecuación:

```
x^n + y^n = z^n
```

para ningún valor entero de `n > 2`.

## Casos Especiales

- **n = 1**: Trivial - infinitas soluciones (ej: 2 + 3 = 5)
- **n = 2**: Tripletas Pitagóricas - infinitas soluciones (ej: 3² + 4² = 5²)
- **n > 2**: **NO HAY SOLUCIONES** - esto es el Último Teorema de Fermat

## Historia de la Demostración

- **1637**: Pierre de Fermat enuncia el teorema
- **1753**: Leonhard Euler demuestra el caso n=3
- **1825**: Sophie Germain y otros demuestran casos especiales
- **1847**: Gabriel Lamé demuestra el caso n=7
- **1995**: **Andrew Wiles** publica la demostración completa

La demostración de Wiles utiliza matemáticas extremadamente avanzadas:
- Curvas elípticas
- Formas modulares
- Representaciones de Galois
- Teoría de números algebraicos

## Verificación Computacional

Aunque no podemos "demostrar" el teorema con código, podemos:
1. Verificar que no existen soluciones para valores pequeños
2. Generar contraejemplos si el teorema fuera falso (no los encontraremos)
3. Visualizar por qué el teorema es verdadero para casos específicos

## Programa de Verificación

Este directorio contiene un programa Python que:
- Busca exhaustivamente posibles soluciones para valores pequeños de n
- Verifica que no existen tripletas que satisfagan la ecuación para n > 2
- Demuestra casos conocidos para n = 1 y n = 2
- Proporciona evidencia computacional (no demostración matemática)

## Uso

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar verificación
python fermat_verifier.py

# Ejecutar con Docker
docker build -t fermat-verifier .
docker run fermat-verifier
```

## Recursos Adicionales

- [Demostración de Andrew Wiles (1995)](https://en.wikipedia.org/wiki/Wiles%27s_proof_of_Fermat%27s_Last_Theorem)
- [Fermat's Last Theorem - Simon Singh](https://en.wikipedia.org/wiki/Fermat%27s_Last_Theorem_(book))
- [Numberphile: Fermat's Last Theorem](https://www.youtube.com/watch?v=qiNcEguuFSA)

## Nota Importante

⚠️ **Este programa NO demuestra el teorema matemáticamente.** La demostración real requiere matemáticas de posgrado y ocupa cientos de páginas. Este es un ejercicio educativo para entender el teorema mediante verificación computacional de casos pequeños.
