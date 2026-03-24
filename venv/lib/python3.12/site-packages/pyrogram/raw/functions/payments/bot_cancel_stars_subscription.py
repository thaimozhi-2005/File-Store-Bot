#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class BotCancelStarsSubscription(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``194``
        - ID: ``57F9ECE6``

    Parameters:
        user_id (:obj:`InputUser <pyrogram.raw.base.InputUser>`):
            N/A

        restore (``bool``, *optional*):
            N/A

        invoice_slug (``str``, *optional*):
            N/A

        charge_id (``str``, *optional*):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["user_id", "restore", "invoice_slug", "charge_id"]

    ID = 0x57f9ece6
    QUALNAME = "functions.payments.BotCancelStarsSubscription"

    def __init__(self, *, user_id: "raw.base.InputUser", restore: Optional[bool] = None, invoice_slug: Optional[str] = None, charge_id: Optional[str] = None) -> None:
        self.user_id = user_id  # InputUser
        self.restore = restore  # flags.0?true
        self.invoice_slug = invoice_slug  # flags.1?string
        self.charge_id = charge_id  # flags.2?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BotCancelStarsSubscription":
        
        flags = Int.read(b)
        
        restore = True if flags & (1 << 0) else False
        user_id = TLObject.read(b)
        
        invoice_slug = String.read(b) if flags & (1 << 1) else None
        charge_id = String.read(b) if flags & (1 << 2) else None
        return BotCancelStarsSubscription(user_id=user_id, restore=restore, invoice_slug=invoice_slug, charge_id=charge_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.restore else 0
        flags |= (1 << 1) if self.invoice_slug is not None else 0
        flags |= (1 << 2) if self.charge_id is not None else 0
        b.write(Int(flags))
        
        b.write(self.user_id.write())
        
        if self.invoice_slug is not None:
            b.write(String(self.invoice_slug))
        
        if self.charge_id is not None:
            b.write(String(self.charge_id))
        
        return b.getvalue()
