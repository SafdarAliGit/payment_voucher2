frappe.ui.form.on('Payment Voucher', {

    refresh: function (frm) {
        function calculate_net_total(frm) {
            var amount = 0;
            $.each(frm.doc.items || [], function (i, d) {
                amount += flt(d.amount);
            });
            frm.set_value("total", amount)
        }

        calculate_net_total(frm)

        frm.set_query("account", function () {
            return {
                filters: [
                    ["Account", "account_type", "in", ["Cash", "Bank"]],
                    ["is_group", "=", 0],
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
    },
    account: function (frm) {
        frappe.call({
            method: 'payment_voucher2.payment_voucher2.doctype.utils.get_account_balance',
            args: {
                account: frm.doc.account,
            },
            callback: function (r) {
                if (!r.exc) {
                    frm.set_value('balance', r.message.balance);
                }
            }
        });
    }
});


frappe.ui.form.on("Payment Voucher Items", {

    account: function (frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        frappe.call({
            method: 'payment_voucher2.payment_voucher2.doctype.utils.get_party_type',
            args: {
                account: d.account,
            },
            callback: function (r) {
                if (!r.exc) {
                    frappe.model.set_value(cdt, cdn, 'party_type', r.message.party_type);
                }
            }
        });
    },
    amount: function (frm, cdt, cdn) {
        function calculate_net_total(frm) {
            var amount = 0;
            $.each(frm.doc.items || [], function (i, d) {
                amount += flt(d.amount);
            });
            frm.set_value("total", amount)
        }

        calculate_net_total(frm)
    },
    items_remove: function (frm) {
        function calculate_net_total(frm) {
            var amount = 0;
            $.each(frm.doc.items || [], function (i, d) {
                amount += flt(d.amount);
            });
            frm.set_value("total", amount)
        }

        calculate_net_total(frm)
        frm.refresh_field('items');
    }

});

