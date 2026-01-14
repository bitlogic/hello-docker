# Receta Flat White ☕

## Descripción

El **Flat White** es una bebida de café originaria de Australia/Nueva Zelanda que se caracteriza por su equilibrio perfecto entre espresso y leche microespumada.

## Ingredientes

- 1 shot de espresso (30ml / 1 oz)
- 150-180ml de leche entera (preferiblemente)
- Una pizca de arte latte (opcional)

## Equipo Necesario

- Máquina de espresso
- Vaporizador de leche (steam wand)
- Jarra de leche (pitcher)
- Taza de 150-180ml (5-6 oz)
- Termómetro (opcional pero recomendado)

## Instrucciones Paso a Paso

### 1. Preparación del Espresso
```
- Moler café fresco (18-20g para un shot doble si prefieres más intensidad)
- Extraer 1 shot de espresso (30ml en 25-30 segundos)
- Verter directamente en la taza precalentada
```

### 2. Preparación de la Leche
```
- Llenar la jarra con leche fría hasta 1cm por debajo del pico
- Introducir el vaporizador justo debajo de la superficie
- Texturizar la leche creando microespuma (no espuma gruesa)
- Calentar hasta 60-65°C (140-150°F)
- La leche debe tener una textura sedosa y brillante
```

### 3. Vertido y Presentación
```
- Golpear suavemente la jarra contra la encimera para eliminar burbujas grandes
- Girar la jarra para mantener la textura homogénea
- Verter la leche sobre el espresso desde una altura de 3-5cm
- A medida que la taza se llena, acercar la jarra y crear el arte latte
- La capa de espuma final debe ser de aproximadamente 0.5cm (muy fina)
```

## Características del Flat White Perfecto

✅ **Textura**: Leche microespumada y sedosa, integrada completamente con el café

✅ **Proporción**: Mayor proporción de café que un latte, menos espuma que un cappuccino

✅ **Temperatura**: Servido entre 60-65°C para apreciar mejor los sabores

✅ **Presentación**: Superficie de microespuma fina con arte latte simple

✅ **Sabor**: Balance perfecto entre el sabor robusto del espresso y la dulzura natural de la leche

## Diferencias con Otras Bebidas

| Característica | Flat White | Latte | Cappuccino |
|---------------|------------|-------|------------|
| Espresso | 1 shot | 1-2 shots | 1 shot |
| Leche | 150ml | 200-250ml | 150ml |
| Espuma | Microespuma fina (0.5cm) | Espuma ligera (1cm) | Espuma abundante (2cm+) |
| Proporción | Más café, menos leche | Más leche | Equilibrado |
| Textura | Muy sedosa | Cremosa | Espumosa |

## Tips Pro

1. **Calidad del Café**: Usa granos de café recién tostados (7-21 días desde el tueste)

2. **Leche Fría**: Siempre comienza con leche fría del refrigerador para mejor control

3. **Técnica de Vaporización**: 
   - Fase 1: Incorporar aire (0-3 segundos)
   - Fase 2: Texturizar (resto del tiempo)

4. **Temperatura**: No sobrecalentar la leche - destruye la dulzura natural

5. **Limpieza**: Limpiar el vaporizador inmediatamente después de cada uso

6. **Práctica**: La consistencia requiere práctica - no te desanimes

## Variaciones

### Flat White Iced
- Mismo espresso
- Leche fría sin vaporizar
- Servir sobre hielo

### Flat White con Saborizante
- Agregar 1 pump de vainilla/caramelo antes del espresso
- Continuar con la receta normal

### Flat White con Leche Alternativa
- Usar leche de avena (mejor para vaporizar)
- Ajustar técnica según la leche elegida

## Solución de Problemas Comunes

❌ **Espuma muy gruesa**: Introduciste demasiado aire al inicio
→ Solución: Limita la fase de aireación a 2-3 segundos

❌ **Leche separada del café**: Leche mal texturizada o muy caliente
→ Solución: Practica la técnica de vaporización y controla temperatura

❌ **Sabor amargo**: Espresso sobre-extraído
→ Solución: Ajusta la molienda o tiempo de extracción

❌ **Sin cuerpo**: Proporción incorrecta
→ Solución: Respeta las medidas de espresso y leche

## Notas Finales

El **Flat White** es una bebida que celebra la calidad del espresso mientras mantiene una textura aterciopelada gracias a la microespuma perfectamente integrada. A diferencia del cappuccino, donde café y espuma están más separados, el Flat White busca la armonía total entre ambos componentes.

**Tiempo total de preparación**: 2-3 minutos

**Nivel de dificultad**: Intermedio

---

*"Un shot de espresso y luego poner leche"* - pero con técnica, precisión y amor por el café. ☕️

---

## Metáfora Docker 🐳

Al igual que un **contenedor Docker** encapsula una aplicación con todas sus dependencias para funcionar perfectamente, un **Flat White** encapsula el espresso con la cantidad justa de leche microespumada para crear una experiencia de café perfecta y consistente cada vez.

**Dockerfile del Flat White:**
```dockerfile
FROM espresso:double-shot
RUN steam --microfoam milk:whole --temp=63C
EXPOSE 65C
CMD ["pour", "--art=latte", "--texture=silky"]
```

**Docker Compose del Flat White:**
```yaml
version: '3'
services:
  espresso:
    image: coffee:arabica
    volumes:
      - beans:/freshly-ground
    ports:
      - "30ml:1oz"
  
  milk:
    image: dairy:whole
    environment:
      - TEMP=63C
      - TEXTURE=microfoam
    depends_on:
      - espresso
```

¡Disfruta tu Flat White! 🎉
