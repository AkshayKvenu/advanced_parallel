# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2016 Amzsys IT Solutions Pvt Ltd
#    (http://www.amzsys.com)
#    info@amzsys.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api, _
# from odoo.tools import amount_to_text_en
            
            
class Invoice(models.Model):
    _inherit = 'account.invoice'
    
    amt_in_words = fields.Char(compute='set_amt_in_words', string="Amount in words")
    amt_in_arabic_words = fields.Char(compute='set_amt_in_arabic_words', string="Amount in words")
    
    delivery_note_no = fields.Char('Delivery Note No.')
    delivery_date = fields.Char('Delivery Date')
    
    def set_amt_in_words(self):
        for inv in self:
            amount, currency = inv.amount_total, 'SAR'
#             amount_in_words = amount_to_text_en.amount_to_text(amount, lang='ar', currency=currency)
            amount_in_words = inv.currency_id.with_context(lang='ar_SY' or 'es_ES').amount_to_text(amount)
            amount_to_arabic = amount_in_words
            
            if currency == 'SAR':
                if 'و' in amount_in_words:
                    amount_in_words = str(amount_in_words).replace('و', 'and')
                    
#                 if 'Zero' in amount_in_words:
#                     amount_in_words = str(amount_in_words).replace('Zero', '')
#                     amount_in_words = str(amount_in_words).replace(' and', '')
#                     amount_in_words = str(amount_in_words).replace('Cents', '')
#                     amount_in_words = str(amount_in_words).replace('Cent', '')
#                 amount_in_words = str(amount_in_words).replace('SAR', '')
#                 amount_in_words = str(amount_in_words).replace('Cents', 'Halalah')
#                 amount_in_words = str(amount_in_words).replace('Cent', 'Halalah')
#             amount_in_words = 'Saudi Riyal ' + amount_in_words + ' Only'
            amount_in_words = amount_in_words + ' Only'
            inv.amt_in_words = amount_in_words
        
    def set_amt_in_arabic_words(self):
        for inv in self:
            amount, currency = inv.amount_total, 'SAR'
#             amount_in_words = amount_to_text_en.amount_to_text(amount, lang='en', currency=currency)
            amount_in_words = inv.currency_id.with_context(lang='ar_SY' or 'es_ES').amount_to_text(amount)
            amount_int = int(round(amount))
            if amount_int %10 ==0:
                amount_in_words = str(amount_in_words).replace('Nine Hundred', 'تسعمائة ')
                amount_in_words = str(amount_in_words).replace('Eight Hundred', 'ثمانمائة ')
                amount_in_words = str(amount_in_words).replace('Seven Hundred', 'سبعمائة ')
                amount_in_words = str(amount_in_words).replace('Six Hundred', 'ستمائة  ')
                amount_in_words = str(amount_in_words).replace('Five Hundred', 'خمسمائة  ')
                amount_in_words = str(amount_in_words).replace('Four Hundred', 'أربعمائة  ')
                amount_in_words = str(amount_in_words).replace('Three Hundred', 'ثلاثمائة  ')
                amount_in_words = str(amount_in_words).replace('Two Hundred', 'مائتان  ')
                amount_in_words = str(amount_in_words).replace('One Hundred', 'مائة  ')
            amount_in_words = str(amount_in_words).replace('One Hundred', 'مائة  و')
            amount_in_words = str(amount_in_words).replace('Two Hundred', 'مائتان  و')
            amount_in_words = str(amount_in_words).replace('Three Hundred', 'ثلاثمائة  و')
            amount_in_words = str(amount_in_words).replace('Four Hundred', 'أربعمائة  و')
            amount_in_words = str(amount_in_words).replace('Five Hundred', 'خمسمائة  و')
            amount_in_words = str(amount_in_words).replace('Six Hundred', 'ستمائة  و')
            amount_in_words = str(amount_in_words).replace('Seven Hundred', 'سبعمائة و')
            amount_in_words = str(amount_in_words).replace('Eight Hundred', 'ثمانمائة و')
            amount_in_words = str(amount_in_words).replace('Nine Hundred', 'تسعمائة و')
                
            if 3000.0 <= amount <= 10000.99 or 103000.0 <= amount <= 110000.99 or 203000.0 <= amount <= 210000.99\
            or 303000.0 <= amount <= 310000.99 or 403000.0 <= amount <= 410000.99 or 503000.0 <= amount <= 510000.99\
            or 603000.0 <= amount <= 610000.99 or 703000.0 <= amount <= 710000.99 or 803000.0 <= amount <= 810000.99\
            or 903000.0 <= amount <= 910000.99 or 1003000.0 <= amount <= 1010000.99: 
                amount_in_words = str(amount_in_words).replace('Thousand', 'الآلاف ')
            if currency == 'SAR':
                amount_in_words = str(amount_in_words).replace('One Million', 'مليون')
                amount_in_words = str(amount_in_words).replace('Two Million', 'مليونان')
                amount_in_words = str(amount_in_words).replace('Million', 'مليون')
                amount_in_words = str(amount_in_words).replace('One Hundred Thousand', ' مئة الف')
                amount_in_words = str(amount_in_words).replace('Two Hundred Thousand', ' مئتي ألف')
                amount_in_words = str(amount_in_words).replace('One Thousand', ' ألف')
                amount_in_words = str(amount_in_words).replace('Two Thousand', ' ألفان')
                amount_in_words = str(amount_in_words).replace('Thousand', 'آلاف ')
                    
                amount_in_words = str(amount_in_words).replace('Ninety-Nine', 'تسعة وتسعون ')
                amount_in_words = str(amount_in_words).replace('Ninety-Eight', 'ثمانية وتسعون ')
                amount_in_words = str(amount_in_words).replace('Ninety-Seven', 'سبعة وتسعون ')
                amount_in_words = str(amount_in_words).replace('Ninety-Six', 'ستة وتسعون ')
                amount_in_words = str(amount_in_words).replace('Ninety-Five', 'خمسة وتسعون ')
                amount_in_words = str(amount_in_words).replace('Ninety-Four', 'أربعة وتسعون ')
                amount_in_words = str(amount_in_words).replace('Ninety-Three', 'ثلاثة وتسعون ')
                amount_in_words = str(amount_in_words).replace('Ninety-Two', 'اثنان وتسعون ')
                amount_in_words = str(amount_in_words).replace('Ninety-One', 'واحد وتسعون')
    
                amount_in_words = str(amount_in_words).replace('Ninety', 'تسعون')
                amount_in_words = str(amount_in_words).replace('Eighty-Nine', 'تسعة وثمانون ')
                amount_in_words = str(amount_in_words).replace('Eighty-Eight', 'ثمانية وثمانون ')
                amount_in_words = str(amount_in_words).replace('Eighty-Seven', 'سبعة وثمانون ')
                amount_in_words = str(amount_in_words).replace('Eighty-Six', 'ستة وثمانون ')
                amount_in_words = str(amount_in_words).replace('Eighty-Five', 'خمسة وثمانون ')
                amount_in_words = str(amount_in_words).replace('Eighty-Four', 'أربعة وثمانون ')
                amount_in_words = str(amount_in_words).replace('Eighty-Three', 'ثلاثة وثمانون ')
                amount_in_words = str(amount_in_words).replace('Eighty-Two', 'اثنان وثمانون ')
                amount_in_words = str(amount_in_words).replace('Eighty-One', ' واحد وثمانون')
    
                amount_in_words = str(amount_in_words).replace('Eighty', 'ثمانون')
                amount_in_words = str(amount_in_words).replace('Seventy-Nine', 'تسعة وسبعون ')
                amount_in_words = str(amount_in_words).replace('Seventy-Eight', 'ثمانية وسبعون ')
                amount_in_words = str(amount_in_words).replace('Seventy-Seven ', 'سبعة وسبعون ')
                amount_in_words = str(amount_in_words).replace('Seventy-Six ', 'ستة وسبعون ')
                amount_in_words = str(amount_in_words).replace('Seventy-Five', 'خمسة وسبعون ')
                amount_in_words = str(amount_in_words).replace('Seventy-Four', 'أربعة وسبعون ')
                amount_in_words = str(amount_in_words).replace('Seventy-Three', 'ثلاثة وسبعون ')
                amount_in_words = str(amount_in_words).replace('Seventy-Two', 'اثنان وسبعون ')
                amount_in_words = str(amount_in_words).replace('Seventy-One', 'واحد وسبعون')
    
                amount_in_words = str(amount_in_words).replace('Seventy', 'سبعون')
                amount_in_words = str(amount_in_words).replace('Sixty-Nine', 'تسعة وستون ')
                amount_in_words = str(amount_in_words).replace('Sixty-Eight', 'ثمانية وستون ')
                amount_in_words = str(amount_in_words).replace('Sixty-Seven', 'سبعة وستون ')
                amount_in_words = str(amount_in_words).replace('Sixty-Six', 'ستة وستون ')
                amount_in_words = str(amount_in_words).replace('Sixty-Five', 'خمسة وستون ')
                amount_in_words = str(amount_in_words).replace('Sixty-Four', 'أربعة وستون ')
                amount_in_words = str(amount_in_words).replace('Sixty-Three', 'ثلاثة وستون ')
                amount_in_words = str(amount_in_words).replace('Sixty-Two', 'اثنان وستون ')
                amount_in_words = str(amount_in_words).replace('Sixty-One', 'واحد وستون')
                amount_in_words = str(amount_in_words).replace('Sixty', 'ستون')
                amount_in_words = str(amount_in_words).replace('Fifty-Nine', 'تسعة وخمسون ')
                amount_in_words = str(amount_in_words).replace('Fifty-Eight', 'ثمانية وخمسون ')
                amount_in_words = str(amount_in_words).replace('Fifty-Seven', 'سبعة وخمسون ')
                amount_in_words = str(amount_in_words).replace('Fifty-Six', 'ستة وخمسون ')
                amount_in_words = str(amount_in_words).replace('Fifty-Five', 'خمسة وخمسون ')
                amount_in_words = str(amount_in_words).replace('Fifty-Four', 'أربعة وخمسون ')
                amount_in_words = str(amount_in_words).replace('Fifty-Three', 'ثلاثة وخمسون ')
                amount_in_words = str(amount_in_words).replace('Fifty-Two', 'اثنان وخمسون ')
                amount_in_words = str(amount_in_words).replace('Fifty-One', 'واحد وخمسون')
    
                amount_in_words = str(amount_in_words).replace('Fifty', 'خمسون')
                amount_in_words = str(amount_in_words).replace('Forty-Nine', 'تسعة وأربعون ')
                amount_in_words = str(amount_in_words).replace('Forty-Eight', 'ثمانة وأربعون ')
                amount_in_words = str(amount_in_words).replace('Forty-Seven', 'سبعة وأربعون')
                amount_in_words = str(amount_in_words).replace('Forty-Six', 'ستة وأربعون')
                amount_in_words = str(amount_in_words).replace('Forty-Five', 'خمسة وأربعون')
                amount_in_words = str(amount_in_words).replace('Forty-Four', 'أربعة وأربعون')
                amount_in_words = str(amount_in_words).replace('Forty-Three', 'ثلاثة وأربعون')
                amount_in_words = str(amount_in_words).replace('Forty-Two', 'اثنان وأربعون')
                amount_in_words = str(amount_in_words).replace('Forty-One', 'واحد وأربعون')
    
                amount_in_words = str(amount_in_words).replace('Forty', 'اربعون')
                amount_in_words = str(amount_in_words).replace('Thirty-Nine', 'تسعة وثلاثون')
                amount_in_words = str(amount_in_words).replace('Thirty-Eight', 'ثمانية وثلاثون')
                amount_in_words = str(amount_in_words).replace('Thirty-Seven ', 'سبعة وثلاثون')
                amount_in_words = str(amount_in_words).replace('Thirty-Six', 'ستة وثلاثون')
                amount_in_words = str(amount_in_words).replace('Thirty-Five ', 'خمسة وثلاثون')
                amount_in_words = str(amount_in_words).replace('Thirty-Four', 'أربعة وثلاثون')
                amount_in_words = str(amount_in_words).replace('Thirty-Three', 'ثلاثة وثلاثون')
                amount_in_words = str(amount_in_words).replace('Thirty-Two', 'اثنان وثلاثون')
                amount_in_words = str(amount_in_words).replace('Thirty-One', 'واحد وثلاثون')
                amount_in_words = str(amount_in_words).replace('Thirty', 'ثلاثون')
                amount_in_words = str(amount_in_words).replace('Twenty-Nine', 'تسعة وعشرون')
                amount_in_words = str(amount_in_words).replace('Twenty-Eight', 'ثمانية وعشرون')
                amount_in_words = str(amount_in_words).replace('Twenty-Seven', 'سبعة وعشرون')
                amount_in_words = str(amount_in_words).replace('Twenty-Six', ' ستة وعشرون')
                amount_in_words = str(amount_in_words).replace('Twenty-Five', ' خمسة وعشرون')
                amount_in_words = str(amount_in_words).replace('Twenty-Four', ' اربعة وعشرون ')
                amount_in_words = str(amount_in_words).replace('Twenty-Three', ' ثلاثة وعشرون ')
                amount_in_words = str(amount_in_words).replace('Twenty-Two', ' اثنى وعشرون')
                amount_in_words = str(amount_in_words).replace('Twenty-One', ' واحد وعشرون')
    
                amount_in_words = str(amount_in_words).replace('Twenty', 'عشرون')
                amount_in_words = str(amount_in_words).replace('Nineteen', 'تسعة عشر')
                amount_in_words = str(amount_in_words).replace('Eighteen', 'ثمانية عشر')
                amount_in_words = str(amount_in_words).replace('Seventeen', 'سبعة عشر')
                amount_in_words = str(amount_in_words).replace('Sixteen', 'ستة عشر')
                amount_in_words = str(amount_in_words).replace('Fifteen', 'خمسة عشر')
                amount_in_words = str(amount_in_words).replace('Fourteen', 'اربعة عشر')
                amount_in_words = str(amount_in_words).replace('Thirteen', 'ثلاثة عشر')
                amount_in_words = str(amount_in_words).replace('Twelve', 'اثنى عشر')
                amount_in_words = str(amount_in_words).replace('Eleven', 'احدى عشر')
                amount_in_words = str(amount_in_words).replace('Ten', 'عشرة')
                amount_in_words = str(amount_in_words).replace('Nine', 'تسعة')
                amount_in_words = str(amount_in_words).replace('Eight', 'ثمانية')
                amount_in_words = str(amount_in_words).replace('Seven', 'سبعة')
                amount_in_words = str(amount_in_words).replace('Six', 'ستة')
                amount_in_words = str(amount_in_words).replace('Five', 'خمسة')
                amount_in_words = str(amount_in_words).replace('Four', 'اربعة')
                amount_in_words = str(amount_in_words).replace('Three', 'ثلاثة')
                amount_in_words = str(amount_in_words).replace('Two', 'اثنان')
                amount_in_words = str(amount_in_words).replace('One', 'واحد')
                if 'Zero' not in amount_in_words:
                    amount_in_words = str(amount_in_words).replace('and',  'و')
                    amount_in_words = str(amount_in_words).replace('And',  'و')
                    amount_in_words = str(amount_in_words).replace('Cents', 'هللة')
                    amount_in_words = str(amount_in_words).replace('Cent', 'هللة')
                amount_in_words = str(amount_in_words).replace('and', '')
                amount_in_words = str(amount_in_words).replace('And', '')
                amount_in_words = str(amount_in_words).replace('Zero', '')
                amount_in_words = str(amount_in_words).replace(',', ' و ')
                amount_in_words = str(amount_in_words).replace('Cents', '')
                amount_in_words = str(amount_in_words).replace('Cent', '')
                amount_in_words = str(amount_in_words).replace('SAR', 'ريال')
                amount_in_words = str(amount_in_words).replace('Riyal', 'الريال')
                
#             amount_in_words =  ' فقط '+ amount_in_words + '  لا غير'
            amount_in_words = amount_in_words + '  لا غير'
            inv.amt_in_arabic_words = amount_in_words
    
    


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
