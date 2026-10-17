/** @odoo-module **/

import { registry } from "@web/core/registry";

/**
 * Odoo muestra el diálogo "Odoo Client Error" ante cualquier rechazo de
 * promesa no controlado, incluidos los que provocan las extensiones del
 * navegador (p. ej. "Could not establish connection. Receiving end does not
 * exist."). Ese mensaje no proviene de Odoo ni del sitio, así que lo
 * ignoramos para no asustar a los visitantes. Los errores reales de Odoo se
 * siguen mostrando con normalidad.
 */
const EXTENSION_ERROR_PATTERNS = [
    "Could not establish connection. Receiving end does not exist.",
    "A listener indicated an asynchronous response by returning true, but the message channel closed",
    "Extension context invalidated",
    "message port closed before a response was received",
];

function isBrowserExtensionError(message) {
    if (!message) {
        return false;
    }
    return EXTENSION_ERROR_PATTERNS.some((pattern) => message.includes(pattern));
}

export function ignoreBrowserExtensionErrors(env, error, originalError) {
    const message = (originalError && originalError.message) || (error && error.message);
    if (!isBrowserExtensionError(message)) {
        return false;
    }
    if (error.unhandledRejectionEvent) {
        error.unhandledRejectionEvent.preventDefault();
    }
    if (error.event) {
        error.event.preventDefault();
    }
    return true;
}

registry
    .category("error_handlers")
    .add("ecuabyteIgnoreBrowserExtensionErrors", ignoreBrowserExtensionErrors, {
        sequence: 1,
    });
