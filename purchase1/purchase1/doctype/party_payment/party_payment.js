cur_frm.cscript.party=function(doc,cdt,cdn)
{
	var party=doc.party;
	frappe.call({
		method:"purchase1.purchase1.doctype.party_payment.party_payment.get_amount",
		args:{party:party},
		callback:function(r)
		{
			cur_frm.set_value("remaining_amount",r.message);
		}
	});
}
cur_frm.cscript.payment_mode=function(doc,cdt,cdn)
{
	var d=doc.payment_mode;
	if(d=='Cash')
	{
		cur_frm.toggle_enable('cheque_no', false);
		cur_frm.toggle_enable('bank', false);
		cur_frm.toggle_enable('bank_name', false);
	}
	else
	{
		cur_frm.toggle_enable('cheque_no', true);
		cur_frm.toggle_enable('bank', true);
		cur_frm.toggle_enable('bank_name', true);
	}
}