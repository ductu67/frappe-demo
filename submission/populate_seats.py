import frappe
import random


def execute():
	# Kiểm tra xem cột 'seat' đã thực sự tồn tại dưới DB chưa
	if not frappe.db.has_column("Airplane Ticket", "seat"):
		print("⚠️ Cột 'seat' chưa tồn tại trong Database. Bỏ qua patch để kiểm tra lại DocType.")
		return

	# Nếu đã có cột 'seat', tiến hành điền dữ liệu như bình thường
	tickets = frappe.get_all("Airplane Ticket", fields=["name", "seat"])

	for ticket in tickets:
		if not ticket.seat:
			random_num = random.randint(1, 99)
			random_letter = random.choice(['A', 'B', 'C', 'D', 'E'])
			generated_seat = f"{random_num}{random_letter}"

			frappe.db.set_value("Airplane Ticket", ticket.name, "seat", generated_seat)

	frappe.db.commit()
	print("✅ Đã hoàn thành điền số ghế cho các vé cũ.")
