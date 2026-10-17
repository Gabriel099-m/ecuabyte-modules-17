# ecuabyte-modules-17

Módulos personalizados de Odoo 17 desarrollados por **Ecuabyte Innovations**.

## Módulos incluidos

### `ecuabyte_inventory_web`
Añade un interruptor (**toggle**) en el listado de productos para publicar o
despublicar productos en la tienda online (`/shop`).

- Campo `x_publish_to_shop` en `product.template`.
- Sincroniza automáticamente con `is_published`.
- **Dependencias:** `product`, `website_sale`.

### `ecuabyte_website_custom`
Personalización del sitio web (home, tickets, formularios) para Ecuabyte.

## Instalación

Copiar la carpeta del módulo dentro del `addons_path` de Odoo y activar el
modo desarrollador, luego:

```bash
odoo-bin -c odoo.conf -d <base_de_datos> -i ecuabyte_inventory_web --stop-after-init
```

O desde la interfaz en **Aplicaciones → Actualizar lista de aplicaciones**.
