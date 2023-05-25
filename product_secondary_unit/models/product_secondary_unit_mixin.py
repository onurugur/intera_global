# Copyright 2021 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.tools.float_utils import float_round


class ProductSecondaryUnitMixin(models.AbstractModel):
    """
    Mixin model that allows to compute a field from a secondary unit helper
    An example is to extend any model in which you want to compute quantities
    based on secondary units. You must add a dictionary `_secondary_unit_fields`
    as class variable with the following content:
    _secondary_unit_fields = {
        "qty_field": "product_uom_qty",
        "uom_field": "product_uom"
    }

    To compute ``qty_field`` on target model, you must convert the field to computed
    writable (computed, stored and readonly=False), and you have to define the
    compute method adding ``secondary_uom_id`` and ``secondary_uom_qty`` fields
    as dependencies and calling inside to ``self._compute_helper_target_field_qty()``.

    To compute secondary units when user changes the uom field on target model,
    you must add an onchange method on uom field and call to
    ``self._onchange_helper_product_uom_for_secondary()``

    You can see an example in ``purchase_order_secondary_unit`` on purchase-workflow
    repository.
    """

    _name = "product.secondary.unit.mixin"
    _description = "Product Secondary Unit Mixin"
    _secondary_unit_fields = {}
    _third_unit_fields = {}
    _fourth_unit_fields = {}

    @api.model
    def _get_default_secondary_uom(self):
        return self.env["product.template"]._get_default_secondary_uom()

    @api.model
    def _get_default_third_uom(self):
        return self.env["product.template"]._get_default_third_uom()

    @api.model
    def _get_default_fourth_uom(self):
        return self.env["product.template"]._get_default_fourth_uom()

    secondary_uom_qty = fields.Float(
        string="Secondary Qty",
        digits="Product Unit of Measure",
        store=True,
        readonly=False,
        compute="_compute_secondary_uom_qty",
        default="1",
    )
    secondary_uom_id = fields.Many2one(
        comodel_name="product.secondary.unit",
        string="Second unit",
        ondelete="restrict",
        default=_get_default_secondary_uom,
    )

    third_uom_qty = fields.Float(
        string="Third Qty",
        digits="Product Unit of Measure",
        store=True,
        readonly=False,
        compute="_compute_secondary_uom_qty",
        default="1",
    )
    third_uom_id = fields.Many2one(
        comodel_name="product.secondary.unit",
        string="Third unit",
        ondelete="restrict",
        default=_get_default_third_uom,
    )

    fourth_uom_qty = fields.Float(
        string="Third Qty",
        digits="Product Unit of Measure",
        store=True,
        readonly=False,
        compute="_compute_secondary_uom_qty",
        default="1",
    )
    fourth_uom_id = fields.Many2one(
        comodel_name="product.secondary.unit",
        string="Fourth unit",
        ondelete="restrict",
        default=_get_default_fourth_uom,
    )

    def _get_uom_line(self,x):
        if x==2:
            return self[self._secondary_unit_fields["uom_field"]]
        if x==3:
            return self[self._third_unit_fields["uom_field"]]
        if x==4:
            return self[self._fourth_unit_fields["uom_field"]]
    def _get_factor_line(self,uom,x):
        return uom.factor * self._get_uom_line(x).factor

    def _get_quantity_from_line(self,x):
        if x==2:
            return self[self._secondary_unit_fields["qty_field"]]
        if x==3:
            return self[self._third_unit_fields["qty_field"]]
        if x==4:
            return self[self._fourth_unit_fields["qty_field"]]

    @api.model
    def _get_secondary_uom_qty_depends(self):
        if not self._secondary_unit_fields:
            return []
        return [self._secondary_unit_fields["qty_field"]]

    @api.model
    def _get_third_uom_qty_depends(self):
        if not self._third_unit_fields:
            return []
        return [self._third_unit_fields["qty_field"]]

    @api.model
    def _get_fourth_uom_qty_depends(self):
        if not self._fourth_unit_fields:
            return []
        return [self._fourth_unit_fields["qty_field"]]

    @api.depends(lambda x: x._get_secondary_uom_qty_depends() and x._get_third_uom_qty_depends() and x._get_fourth_uom_qty_depends())
    def _compute_secondary_uom_qty(self):
        for line in self:
            if not line.secondary_uom_id:
                line.secondary_uom_qty = 0.0
                continue
            elif line.secondary_uom_id.dependency_type == "independent":
                continue
            factor = line._get_factor_line(line.secondary_uom_id,2)
            qty_line = line._get_quantity_from_line(2)
            qty = float_round(
                qty_line / (factor or 1.0),
                precision_rounding=line.secondary_uom_id.uom_id.rounding,
            )
            line.third_uom_qty = qty
            if not line.third_uom_id:
                line.third_uom_qty = 0.0
                continue
            elif line.third_uom_id.dependency_type == "independent":
                continue
            factor = line._get_factor_line(line.third_uom_id,3)
            qty_line = line._get_quantity_from_line(3)
            qty = float_round(
                qty_line / (factor or 1.0),
                precision_rounding=line.third_uom_id.uom_id.rounding,
            )
            line.third_uom_qty = qty
            if not line.fourth_uom_id:
                line.third_uom_qty = 0.0
                continue
            elif line.fourth_uom_id.dependency_type == "independent":
                continue
            factor = line._get_factor_line(line.fourth_uom_id,4)
            qty_line = line._get_quantity_from_line(4)
            qty = float_round(
                qty_line / (factor or 1.0),
                precision_rounding=line.fourth_uom_id.uom_id.rounding,
            )
            line.fourth_uom_qty = qty


    def _compute_helper_target_field_qty(self):
        """Set the target qty field defined in model"""
        for rec in self:
            if not rec.secondary_uom_id:
                rec[rec._secondary_unit_fields["qty_field"]] = rec._origin[
                    rec._secondary_unit_fields["qty_field"]
                ]
                continue
            if rec.secondary_uom_id.dependency_type == "independent":
                if rec[rec._secondary_unit_fields["qty_field"]] == 0.0:
                    rec[rec._secondary_unit_fields["qty_field"]] = 1.0
                continue
            # To avoid recompute secondary_uom_qty field when
            # secondary_uom_id changes.
            rec.env.remove_to_compute(
                field=rec._fields["secondary_uom_qty"], records=rec
            )
            factor = rec._get_factor_line(rec.secondary_uom_id,2)
            qty = float_round(
                rec.secondary_uom_qty * factor,
                precision_rounding=rec._get_uom_line(2).rounding,
            )
            rec[rec._secondary_unit_fields["qty_field"]] = qty

            if not rec.third_uom_id:
                rec[rec._third_unit_fields["qty_field"]] = rec._origin[
                    rec._third_unit_fields["qty_field"]
                ]
                continue
            if rec.third_uom_id.dependency_type == "independent":
                if rec[rec._third_unit_fields["qty_field"]] == 0.0:
                    rec[rec._third_unit_fields["qty_field"]] = 1.0
                continue
                # To avoid recompute secondary_uom_qty field when
                # secondary_uom_id changes.
            rec.env.remove_to_compute(
                field=rec._fields["third_uom_qty"], records=rec
            )
            factor = rec._get_factor_line(rec.third_uom_id,3)
            qty = float_round(
                rec.third_uom_qty * factor,
                precision_rounding=rec._get_uom_line(3).rounding,
            )
            rec[rec._third_unit_fields["qty_field"]] = qty
            if not rec.fourth_uom_id:
                rec[rec._fourth_unit_fields["qty_field"]] = rec._origin[
                    rec._fourth_unit_fields["qty_field"]
                ]
                continue
            if rec.fourth_uom_id.dependency_type == "independent":
                if rec[rec._fourth_unit_fields["qty_field"]] == 0.0:
                    rec[rec._fourth_unit_fields["qty_field"]] = 1.0
                continue
                # To avoid recompute secondary_uom_qty field when
                # secondary_uom_id changes.
            rec.env.remove_to_compute(
                field=rec._fields["fourth_uom_qty"], records=rec
            )
            factor = rec._get_factor_line(rec.fourth_uom_id, 4)
            qty = float_round(
                rec.third_uom_qty * factor,
                precision_rounding=rec._get_uom_line(3).rounding,
            )
            rec[rec._third_unit_fields["qty_field"]] = qty

    def _onchange_helper_product_uom_for_secondary(self):
        """Helper method to be called from onchange method of uom field in
        target model.
        """
        if not self.secondary_uom_id:
            self.secondary_uom_qty = 0.0
            return
        elif self.secondary_uom_id.dependency_type == "independent":
            return
        factor = self._get_factor_line(self.secondary_uom_id,2)
        line_qty = self._get_quantity_from_line(2)
        qty = float_round(
            line_qty / (factor or 1.0),
            precision_rounding=self._get_uom_line(2).rounding,
        )
        self.secondary_uom_qty = qty
        if not self.third_uom_id:
            self.third_uom_qty = 0.0
            return
        elif self.third_uom_id.dependency_type == "independent":
            return
        factor = self._get_factor_line(self.third_uom_id,3)
        line_qty = self._get_quantity_from_line(3)
        qty = float_round(
            line_qty / (factor or 1.0),
            precision_rounding=self._get_uom_line().rounding,
        )
        self.third_uom_qty = qty
        if not self.fourth_uom_id:
            self.fourth_uom_qty = 0.0
            return
        elif self.fourth_uom_id.dependency_type == "independent":
            return
        factor = self._get_factor_line(self.fourth_uom_id,4)
        line_qty = self._get_quantity_from_line(4)
        qty = float_round(
            line_qty / (factor or 1.0),
            precision_rounding=self._get_uom_line(4).rounding,
        )
        self.fourth_uom_qty = qty