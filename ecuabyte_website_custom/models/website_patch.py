# -*- coding: utf-8 -*-
import json

from odoo import api, models
from odoo.tools.misc import file_path


# Traducciones de los tipos de identificacion (l10n_latam.identification.type).
# source (en_US) -> es / pt
IDENTIFICATION_TYPE_TRANSLATIONS = {
    # Genericos (l10n_latam_base)
    'l10n_latam_base.it_vat': {'es_EC': 'IVA', 'pt_PT': 'IVA'},
    'l10n_latam_base.it_pass': {'es_EC': 'Pasaporte', 'pt_PT': 'Passaporte'},
    'l10n_latam_base.it_fid': {'es_EC': 'Cédula Extranjera', 'pt_PT': 'Cédula Estrangeira'},
    # Ecuador (l10n_ec)
    'l10n_ec.ec_ruc': {'es_EC': 'RUC', 'pt_PT': 'RUC'},
    'l10n_ec.ec_dni': {'es_EC': 'Cédula', 'pt_PT': 'Cédula'},
    'l10n_ec.ec_passport': {'es_EC': 'Pasaporte', 'pt_PT': 'Passaporte'},
    'l10n_ec.ec_unknown': {'es_EC': 'Desconocido', 'pt_PT': 'Desconhecido'},
}

# Etiquetas del checkout de Ecuador (l10n_ec_website_sale) a re-traducir.
L10N_EC_TEMPLATE_TRANSLATIONS = {
    'l10n_ec_website_sale.partner_info': {
        'es_EC': {
            'Identification Type': 'Tipo de Identificación',
        },
        'pt_PT': {
            'Identification Type': 'Tipo de Identificação',
            'Changing Identification type is not allowed once document(s) '
            'have been issued for your account. Please contact us directly '
            'for this operation.':
                'Não é permitido alterar o tipo de identificação após a emissão '
                'de documentos para a sua conta. Contacte-nos diretamente para '
                'esta operação.',
        },
    },
    'l10n_ec_website_sale.address': {
        'es_EC': {
            'Identification Number': 'Número de Identificación',
        },
        'pt_PT': {
            'Identification Number': 'Número de Identificação',
        },
    },
}


class EcuabyteWebsitePatch(models.AbstractModel):
    _name = 'ecuabyte.website.patch'
    _description = 'Ecuabyte website translations patcher'

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    @api.model
    def _read_resource(self, filename):
        path = file_path('ecuabyte_website_custom/data/%s' % filename)
        with open(path, 'r', encoding='utf-8') as handle:
            return handle.read().rstrip('\n')

    @api.model
    def _available_languages(self):
        codes = self.env['res.lang'].sudo().search([]).mapped('code')
        return set(codes) | {'en_US'}

    @api.model
    def _patch_view(self, view, prefix):
        """Set the ES / EN / PT arch of ``view`` from ``<prefix>_<lang>.html``.

        ``arch_db`` uses ``translate=xml_translate`` (a callable), so the full
        arch per language is stored in the jsonb column.  We merge the wanted
        languages directly (keeping any other language untouched) and refresh
        the record + caches afterwards.
        """
        lang_files = {
            'es_EC': '%s_es_EC.html' % prefix,
            'en_US': '%s_en_US.html' % prefix,
            'pt_PT': '%s_pt_PT.html' % prefix,
        }
        available = self._available_languages()
        translations = {
            lang: self._read_resource(filename)
            for lang, filename in lang_files.items()
            if lang in available
        }
        if not translations:
            return False
        self.env.cr.execute(
            "UPDATE ir_ui_view SET arch_db = arch_db || %s::jsonb WHERE id = %s",
            (json.dumps(translations), view.id),
        )
        view.invalidate_recordset(['arch_db'])
        view.modified(['arch_db'])
        return True

    @api.model
    def _get_raw_arch(self, view):
        """Return the whole ``arch_db`` jsonb dict (lang -> arch) of a view."""
        self.env.cr.execute(
            "SELECT arch_db FROM ir_ui_view WHERE id = %s", (view.id,))
        row = self.env.cr.fetchone()
        return (row and row[0]) or {}

    @api.model
    def _merge_arch(self, view, translations):
        if not translations:
            return False
        self.env.cr.execute(
            "UPDATE ir_ui_view SET arch_db = arch_db || %s::jsonb WHERE id = %s",
            (json.dumps(translations), view.id),
        )
        view.invalidate_recordset(['arch_db'])
        view.modified(['arch_db'])
        return True

    # ------------------------------------------------------------------
    # step 1: identificacion
    # ------------------------------------------------------------------
    @api.model
    def _translate_identification_types(self):
        available = self._available_languages()
        for xmlid, translations in IDENTIFICATION_TYPE_TRANSLATIONS.items():
            record = self.env.ref(xmlid, raise_if_not_found=False)
            if not record:
                continue
            for lang, value in translations.items():
                if lang in available:
                    record.with_context(lang=lang).write({'name': value})
        return True

    @api.model
    def _ensure_identification_types(self):
        """Activa el tipo 'Pasaporte' de Ecuador para clientes extranjeros."""
        passport = self.env.ref('l10n_ec.ec_passport', raise_if_not_found=False)
        if passport and not passport.active:
            passport.active = True
        return True

    # ------------------------------------------------------------------
    # step 2: etiquetas del checkout de Ecuador
    # ------------------------------------------------------------------
    @api.model
    def _translate_l10n_ec_templates(self):
        available = self._available_languages()
        for xmlid, lang_map in L10N_EC_TEMPLATE_TRANSLATIONS.items():
            view = self.env.ref(xmlid, raise_if_not_found=False)
            if not view:
                continue
            arch_map = self._get_raw_arch(view)
            base = arch_map.get('en_US') or next(iter(arch_map.values()), '')
            if not base:
                continue
            translations = {}
            for lang, replacements in lang_map.items():
                if lang not in available:
                    continue
                arch = base
                for source, target in replacements.items():
                    arch = arch.replace(source, target)
                translations[lang] = arch
            self._merge_arch(view, translations)
        return True

    # ------------------------------------------------------------------
    # main entry point
    # ------------------------------------------------------------------
    @api.model
    def apply_website_translations(self):
        View = self.env['ir.ui.view'].sudo()

        # ---- Home (page with url "/") ---------------------------------
        home_view = View
        pages = self.env['website.page'].sudo().search(
            [('url', '=', '/'), ('website_id', '!=', False)], order='id')
        for candidate in pages:
            if candidate.view_id.key == 'website.homepage':
                home_view = candidate.view_id
                break
        else:
            if pages:
                home_view = pages[0].view_id
        if home_view:
            self._patch_view(home_view, 'home')

        # ---- Helpdesk ticket form ------------------------------------
        ticket_view = self.env.ref(
            'website_helpdesk.ticket_submit_form', raise_if_not_found=False)
        if ticket_view:
            self._patch_view(ticket_view, 'ticket')

        # ---- Checkout: tipos de identificacion + etiquetas EC --------
        self._translate_identification_types()
        self._ensure_identification_types()
        self._translate_l10n_ec_templates()

        # refresh compiled template caches
        self.env.registry.clear_cache()
        return True
