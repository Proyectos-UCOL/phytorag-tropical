# Evidencia manual de COFEPRIS para Exalt

`Consulta_COFEPRIS_Exalt.png` no se descarga automáticamente porque la consulta
oficial requiere interacción manual y la captura forma parte de la evidencia
visual revisada.

La reproducción con el SHA-256 esperado requiere el archivo exacto
`Consulta_COFEPRIS_Exalt.png` entregado dentro de
`data-m1-corpus-revisado.zip`. Volver a consultar COFEPRIS y tomar otra captura
desde el navegador no garantiza el mismo archivo ni el mismo SHA-256, aunque se
use el mismo registro y la misma consulta. Si no se dispone del ZIP, el archivo
debe entregarse por un canal separado antes de ejecutar la reproducción exacta.

1. Abra:
   `https://siipris03.cofepris.gob.mx/Resoluciones/Consultas/ConWebRegPlaguicida.asp`
2. Consulte el registro:
   `RSCO-INAC-0103X-301-064-006`.
3. Capture el detalle completo donde sean legibles el registro, empresa,
   ingrediente activo, nombres comerciales, cultivos listados y vigencia.
4. Guarde la captura exactamente como:
   `data/raw/Consulta_COFEPRIS_Exalt.png`.
5. Verifique el SHA-256:
   `8cd075a2dbe5028c92928269a224a85153cbf08b006a1facaa0c54df427dd847`.

La fecha de consulta debe registrarse en la documentación de revisión; no se
debe inventar a partir de la fecha de modificación del archivo. Si la captura
falta o su hash cambia, `python src/data_ingest.py` se detiene y explica el
paso pendiente. Esta captura no aporta por sí sola dosis, plaga por cultivo,
intervalo de seguridad ni reentrada.
