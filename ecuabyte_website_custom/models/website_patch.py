# -*- coding: utf-8 -*-
import json

from odoo import api, models
from odoo.modules.module import get_module_resource


class EcuabyteWebsitePatch(models.AbstractModel):
    _name = 'ecuabyte.website.patch'
    _description = 'Ecuabyte website translations patcher'

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    @api.model
    def _read_resource(self, filename):
        path = get_module_resource('ecuabyte_website_custom', 'data', filename)
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

        # refresh compiled template caches
        self.env.registry.clear_cache()
        return True
