import frappe
# import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from general_voucher.general_voucher.doctype.utils_functions import get_doctype_by_field


class FundsTransferVoucher(Document):
    def account_type(self):
        account = frappe.get_doc("Account", self.account)
        if account.is_group == 0:
            return account.account_type
        else:
            return None

    def on_submit(self):
        account_type = self.account_type()
        if account_type:
            if account_type == "Cash":
                je_present = get_doctype_by_field('Journal Entry', 'slip_no', self.name)
                company = self.company
                cost_center = frappe.get_cached_value("Company", company, "cost_center")
                cash_account = self.account
                posting_date = self.posting_date
                voucher_type = "Cash Entry"
                crv_no = self.name
                total = self.total
                if len(self.items) > 0 and int(self.ft_status) < 1 and not je_present:
                    je = frappe.new_doc("Journal Entry")
                    je.posting_date = posting_date
                    je.voucher_type = voucher_type
                    je.company = company
                    je.slip_no = crv_no
                    for item in self.items:
                        je.append("accounts", {
                            'account': item.account,
                            'user_remark': item.description,
                            'debit_in_account_currency': item.amount,
                            'credit_in_account_currency': 0,
                            'cost_center': cost_center,
                            'project':item.project,
                            'cost_center':item.cost_center


                        })
                        je.append("accounts", {
                            'account': cash_account,
                            'debit_in_account_currency': 0,
                            'user_remark': f"{item.description if item.description else ''}",
                            'credit_in_account_currency': item.amount,
                            'cost_center': cost_center,
                            'project':item.project,
                            'cost_center':item.cost_center
                        })
                    je.submit()
                    frappe.db.set_value('Funds Transfer Voucher', self.name, 'ft_status', 1)
                else:
                    if len(self.items) < 1:
                        frappe.throw("No detailed rows found")
                    if self.ft_status > 0:
                        frappe.throw("Journal entry already created")
            elif account_type == "Bank":
                je_present = get_doctype_by_field('Journal Entry', 'slip_no', self.name)
                company = self.company
                cost_center = frappe.get_cached_value("Company", company, "cost_center")
                bank_account = self.account
                posting_date = self.posting_date
                voucher_type = "Bank Entry"
                crv_no = self.name
                cheque_no = crv_no
                cheque_date = posting_date
                total = self.total
                if len(self.items) > 0 and int(self.ft_status) < 1 and not je_present:
                    je = frappe.new_doc("Journal Entry")
                    je.posting_date = posting_date
                    je.voucher_type = voucher_type
                    je.company = company
                    je.slip_no = crv_no
                    je.cheque_no = cheque_no,
                    je.cheque_date = cheque_date,
                    for item in self.items:
                        je.append("accounts", {
                            'account': item.account,
                            'user_remark': f"{item.description}, Ref:{item.ref_no}",
                            'debit_in_account_currency': item.amount,
                            'credit_in_account_currency': 0,
                            'cost_center': cost_center,
                            'project':item.project,
                            'cost_center':item.cost_center

                        })
                        je.append("accounts", {
                            'account': bank_account,
                            'debit_in_account_currency': 0,
                            'user_remark': f"{item.description}, Ref:{item.ref_no}",
                            'credit_in_account_currency': item.amount,
                            'cost_center': cost_center,
                            'project':item.project,
                            'cost_center':item.cost_center
                        })
                    je.submit()
                    frappe.db.set_value('Funds Transfer Voucher', self.name, 'ft_status', 1)
                else:
                    if len(self.items) < 1:
                        frappe.throw("No detailed rows found")
                    if self.ft_status > 0:
                        frappe.throw("Journal entry already created")
        else:
            frappe.throw("Account type not found")

    def on_cancel(self):
        try:
            self.ft_status = 0
            current_je = get_doctype_by_field('Journal Entry', 'slip_no', self.name)
            if current_je.docstatus != 2:  # Ensure the document is in the "Submitted" state
                current_je.cancel()
                frappe.db.commit()
            else:
                frappe.throw("Document is not in the 'Submitted' state.")
            if current_je.amended_from:
                new_name = int(current_je.name.split("-")[-1]) + 1
            else:
                new_name = f"{current_je.name}-{1}"
            make_autoname(new_name, 'Jouranl Entry')
        except Exception as e:
            frappe.throw(f"Error canceling Funds Transfer Voucher {self.name}: {str(e)}")
