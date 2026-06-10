# Copyright (c) 2026, Tund and contributors
# For license information, please see license.txt

import frappe
import random
from frappe.model.document import Document
from frappe.utils import flt

class AirplaneTicket(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from airplane_mode.airplane_mode.doctype.airplane_ticket_add_on_item.airplane_ticket_add_on_item import AirplaneTicketAddonItem
		from frappe.types import DF

		add_ons: DF.Table[AirplaneTicketAddonItem]
		amended_from: DF.Link | None
		departure_date: DF.Date
		departure_time: DF.Time
		destination_airport: DF.Link
		destination_airport_code: DF.Data
		duration_of_flight: DF.Duration
		flight: DF.Link
		flight_price: DF.Currency
		passenger: DF.Link
		seat: DF.Data | None
		source_airport: DF.Link
		source_airport_code: DF.Data
		status: DF.Literal["Booked", "Checked-In", "Boarded"]
		total_amount: DF.Currency
	# end: auto-generated types

	_DOCTYPE_NAME = "Airplane Ticket"

	def validate(self):
		pass
		# 1. remove duplicate add-on items
		self.remove_duplicate_add_ons()
		# 2. calculate total amount
		self.calculate_total_amount()


	def calculate_total_amount(self):
		total = flt(self.flight_price or 0)
		for add_on in self.add_ons:
			total += flt(add_on.amount or 0)
		self.total_amount = total


	def remove_duplicate_add_ons(self):
		seen_types = set()
		unique_add_ons = []
		for add_on in self.add_ons:
			if add_on.item not in seen_types:
				seen_types.add(add_on.item)
				unique_add_ons.append(add_on)
		self.add_ons = unique_add_ons

	def before_submit(self):
		# prevent submission if the ticket is already boarded
		if self.status != "Boarded":
			frappe.throw("Only tickets with status 'Boarded' can be submitted.")


	def before_insert(self):
		# assign a random seat number when the ticket is created
		random_number = random.randint(1, 99)
		random_letter = random.choice(['A', 'B', 'C', 'D', 'E', 'F'])
		self.seat = f"{random_number}{random_letter}"
