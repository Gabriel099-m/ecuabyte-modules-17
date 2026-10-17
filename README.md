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
Personalización reproducible del sitio web (home, tickets y checkout), con
contenido en **español (es_EC), inglés (en_US) y portugués (pt_PT)**.

- **Home** (url `/`): contenido ES / EN / PT.
- **Formulario de ticket** (`website_helpdesk.ticket_submit_form`): etiquetas
  ES / EN / PT.
- **Checkout** (`/shop/address`):
  - Tipos de identificación del Ecuador (**RUC, Cédula, Pasaporte**) traducidos
    a ES / EN / PT. Se ocultan los tipos genéricos *VAT*, *Passport* y
    *Foreign ID*.
  - Activa el tipo `l10n_ec.ec_passport` (Pasaporte) y aplica las traducciones
    mediante un parche de modelo.
  - Campo **Compañía** marcado como opcional y a ancho completo.
  - Formulario de dirección en **2 columnas** (1 columna en pantallas < 768px).
- **Filtro de errores de extensiones del navegador**: evita que Odoo muestre el
  diálogo *"Odoo Client Error"* cuando el rechazo de promesa proviene de una
  extensión del navegador (p. ej. *"Could not establish connection. Receiving
  end does not exist."*). Los errores reales de Odoo se siguen mostrando.
- **Dependencias:** `website`, `website_sale`, `l10n_ec_website_sale`.

## Instalación

Copiar la carpeta del módulo dentro del `addons_path` de Odoo y activar el
modo desarrollador, luego:

```bash
odoo-bin -c odoo.conf -d <base_de_datos> -i ecuabyte_inventory_web,ecuabyte_website_custom --stop-after-init
```

O desde la interfaz en **Aplicaciones → Actualizar lista de aplicaciones**.

> Nota: el módulo `ecuabyte_website_custom` requiere los idiomas `es_EC` y
> `pt_PT` activos en la base de datos y en el sitio web para mostrar el
> contenido y las traducciones del checkout.
