// Copyright (c) 2024, Tech Ventures and contributors
// For license information, please see license.txt

frappe.ui.form.on('Journal Voucher', {
    refresh: function (frm) {
        frm.set_query("account", function () {
            return {
                filters: [
                    ["Account", "is_group", "=", 0],
                    ["company", "=", frm.doc.company]
                ]
            };
        });
        frm.set_query('account', 'items', function (doc, cdt, cdn) {
            var d = locals[cdt][cdn];
            return {
                filters: [
                    ["Account", "company", "=", frm.doc.company]
                ]
            };
        });
    }
});
