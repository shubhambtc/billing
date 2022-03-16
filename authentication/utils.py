from fpdf import FPDF
genes = {
    "paddy":"100610",
    "paddy sarbati" : "100610",
    "paddy sugandh" : "100610",
    "paddy 1509" : "100610",
    "paddy RS10" : "100610",
    "paddy 1121" : "100610",
    "paddy 1718" : "100610",
    "maize" : "100590",
    "bajra" : "100829",
    "wheat" : "100110",
    "mustard_seed" : "120750",
}
gstin = {
    "mustard_seed":5
}
def round_school(x):
    i, f = divmod(x, 1)
    return int(i + ((f >= 0.5) if (x > 0) else (f > 0.5)))
def number_to_word(number):
    def get_word(n):
        words={ 0:"", 1:"One", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six", 7:"Seven", 8:"Eight", 9:"Nine", 10:"Ten", 11:"Eleven", 12:"Twelve", 13:"Thirteen", 14:"Fourteen", 15:"Fifteen", 16:"Sixteen", 17:"Seventeen", 18:"Eighteen", 19:"Nineteen", 20:"Twenty", 30:"Thirty", 40:"Forty", 50:"Fifty", 60:"Sixty", 70:"Seventy", 80:"Eighty", 90:"Ninty" }
        if n<=20:
            return words[n]
        else:
            ones=n%10
            tens=n-ones
            return words[tens]+" "+words[ones]
            
    def get_all_word(n):
        d=[100,10,100,100]
        v=["","Hundred","Thousand","lakh"]
        w=[]
        for i,x in zip(d,v):
            t=get_word(n%i)
            if t!="":
                t+=" "+x
            w.append(t.rstrip(" "))
            n=n//i
        w.reverse()

        w=' '.join(w).strip()
        if w.endswith("And"):
            w=w[:-3]
        return w

    arr=str(number).split(".")
    number=int(arr[0])
    crore=number//10000000
    number=number%10000000
    word=""
    if crore>0:
        word+=get_all_word(crore)
        word+=" crore "
    word+=get_all_word(number).strip()+" Rupees" 
    return word + " Only"



class PDF(FPDF):
    all_details = {}

    def side_border(self):
        self.add_page()
        self.line(15, 15, 195, 15)
        self.line(15, 282, 195, 282)
        self.line(195, 15, 195, 282)
        self.line(15, 15, 15, 282)
    
    def mandi_in_internal_border(self):
        self.line(15, 25, 195, 25)
        self.line(15, 70, 195, 70)
        self.line(15, 77, 195, 77)
        self.line(15, 92, 195, 92)
        self.line(15, 100, 195, 100)
        self.line(15, 130, 195, 130)
        self.line(15, 140, 195, 140)
        self.line(15, 195, 195, 195)
        self.line(15, 219, 195, 219)
        self.line(15, 235, 195, 235)
        self.line(15, 252, 195, 252)
        self.line(105,185,145,185)
        self.line(25,201,145,201)
        self.line(25,207,145,207)
        self.line(25,213,145,213)
        self.line(25,219,145,219)
        self.line(145,227,195,227)
        self.line(145,203,195,203)
        self.line(145,211,195,211)
        self.line(55,195,55,219)
        self.line(85,195,85,219)
        self.line(125,195,125,219)
        self.line(105,77,105,219)
        self.line(25,130,25,219)
        self.line(85,130,85,195)
        self.line(125,130,125,195)
        self.line(145,130,145,235)
        self.line(170,130,170,252)
        self.line(135,235,135,252)
        self.line(135,252,135,282)
        self.line(80,252,80,282)
    
    def company_name(self,obj):
        self.set_font('Times', 'B', 22)
        self.set_xy(15,25)
        self.cell(180, 15, obj['name'].upper(), 0, 1, 'C')
        self.set_font('Arial', '', 15)
        self.cell(195, 10, "Commision Agents", 0, 1, 'C')
        self.cell(195, 10, obj['address'].title(), 0, 1, 'C')
        self.cell(195, 10, "Mob: %s             Mob: %s" % (obj['mobile1'], obj['mobile2']), 0, 1, 'C')
        self.set_xy(15,15)
        self.set_font('Arial', '', 12)
        self.cell(50,10,"GSTIN: "+obj['gstin'].upper(), 0,0,'L')
        self.pre_authenticated(obj['name'].title())
        self.signatory(obj['name'].title())
        self.terms_conditions()
        bank_dict = {
            "bank_name": obj['bank_name'],
            "bank_ifsc": obj['bank_ifsc'],
            "bank_account_no": obj['bank_account_no'],
            "bank_branch": obj['bank_branch'],
        }
        self.bank_details(bank_dict)
    
    def set_bill_type(self, bill_type):
        self.set_font('Arial', '', 12)
        self.set_xy(145,15)
        self.cell(50,10,bill_type, 0,0,'R')
        self.set_font('Arial', 'B', 12)
        self.set_xy(15,70)
        self.cell(180,7,"Bill of Supply", 0,0,'C')
    
    def set_date_vehicle(self, inv, date, vehicle):
        self.set_font('Arial', 'B', 12)
        self.set_xy(15, 77)
        self.cell(40,7.5, "Serial No :", 0, 0,'L')
        self.set_xy(55, 77)
        self.set_font('Arial', '', 12)
        self.cell(50,7.5, str(inv), 0, 0,'L')
        self.set_xy(15, 84.5)
        self.set_font('Arial', 'B', 12)
        self.cell(40,7.5, "Date of Issue:", 0, 0,'L')
        self.set_xy(55, 84.5)
        self.set_font('Arial', '', 12)
        self.cell(50,7.5, date, 0, 0,'L')
        self.set_xy(105, 77)
        self.set_font('Arial', 'B', 12)
        self.cell(40,7.5, "Transportation Mode :", 0, 0,'L')
        self.set_xy(155, 77)
        self.set_font('Arial', '', 12)
        self.cell(40,7.5, "By Road", 0, 0,'L')
        self.set_xy(105, 84.5)
        self.set_font('Arial', 'B', 12)
        self.cell(40,7.5, "Vehicle No:", 0, 0,'L')
        self.set_xy(155, 84.5)
        self.set_font('Arial', '', 12)
        self.cell(40,7.5, vehicle if vehicle else "", 0, 0,'L')
    
    def set_detail(self, bill_to,ship_to):
        self.set_font('Arial', 'B', 12)
        self.set_xy(15,92)
        self.cell(90,8,"Details of Reciever/Billed To :", 0, 0,'C')
        self.set_font('Arial', 'B', 12)
        self.set_xy(105,92)
        self.cell(90,8,"Details of consignee/Shipped To :", 0, 0,'C')
        self.billed_to(bill_to)
        self.shipped_to(ship_to)
    
    def billed_to(self, bill_to):
        self.set_font('Arial', 'B', 12)
        self.set_xy(15,100)
        self.cell(20,6,"Name :", 0, 0,'L')
        self.set_xy(35,100)
        if bill_to['id'] == 12 or bill_to['id'] == 16:
            self.set_font('Arial', '', 10)
        else:
            self.set_font('Arial','',12)
        self.cell(70,6,bill_to['name'].title(), 0, 0,'L')
        self.set_xy(15,106)
        self.set_font('Arial', 'B', 12)
        self.cell(20,6,"Address :", 0, 0,'L')
        self.set_xy(35,106)
        self.set_font('Arial', '', 12)
        self.multi_cell(70,6,bill_to['address'].title(), 0, 0,'L')
        self.set_xy(15,118)
        self.set_font('Arial', 'B', 12)
        self.cell(20,6,"State :", 0, 0,'L')
        self.set_xy(35,118)
        self.set_font('Arial', '', 12)
        self.cell(70,6,bill_to['state'].title(), 0, 0,'L')
        self.set_xy(85,118)
        self.cell(20,6,"State Code : %s" %(bill_to['state_code']), 0, 0, 'R')
        self.set_xy(15,124)
        self.set_font('Arial', 'B', 12)
        self.cell(20,6,"GSTIN :", 0, 0,'L')
        self.set_xy(35,124)
        self.set_font('Arial', '', 12)
        x = bill_to['gstin'].upper() if bill_to['gstin'] else ""
        self.cell(70,6,x, 0, 0,'L')

    def shipped_to(self, bill_to):
        self.set_font('Arial', 'B', 12)
        self.set_xy(105,100)
        self.cell(20,6,"Name :", 0, 0,'L')
        self.set_font('Arial', '', 12)
        self.set_xy(125,100)
        self.cell(70,6,bill_to['name'].title(), 0, 0,'L')
        self.set_xy(105,106)
        self.set_font('Arial', 'B', 12)
        self.cell(20,6,"Address :", 0, 0,'L')
        self.set_xy(125,106)
        self.set_font('Arial', '', 12)
        self.multi_cell(70,6,bill_to['address'].title(), 0, 0,'L')
        self.set_xy(105,118)
        self.set_font('Arial', 'B', 12)
        self.cell(20,6,"State :", 0, 0,'L')
        self.set_xy(125,118)
        self.set_font('Arial', '', 12)
        self.cell(70,6,bill_to['state'].title(), 0, 0,'L')
        self.set_xy(175,118)
        self.cell(20,6,"State Code : %s" %(bill_to['state_code']), 0, 0, 'R')
        self.set_xy(105,124)
        self.set_font('Arial', 'B', 12)
        self.cell(20,6,"GSTIN :", 0, 0,'L')
        self.set_xy(125,124)
        self.set_font('Arial', '', 12)
        x = bill_to['gstin'].upper() if bill_to['gstin'] else " "
        self.cell(70,6,x, 0, 0,'L')
        self.set_thead()

    def set_thead(self):
        self.set_xy(15,130)
        self.set_font('Arial', 'B', 10)
        self.cell(10,10,"S.No.", 0, 0,'C')
        self.set_xy(25,130)
        self.set_font('Arial', 'B', 12)
        self.cell(60,10,"Description of Goods", 0, 0,'C')
        self.set_xy(85,130)
        self.cell(20,5,"HSN", 0, 0,'C')
        self.set_xy(85,135)
        self.cell(20,5,"Code", 0, 0,'C')
        self.set_xy(105,130)
        self.cell(20,10,"UOM", 0, 0,'C')
        self.set_xy(125,130)
        self.cell(20,10,"QTY", 0, 0,'C')
        self.set_xy(145,130)
        self.cell(25,10,"Rate", 0, 0,'C')
        self.set_xy(170,130)
        self.cell(25,10,"Amount", 0, 0,'C')
    
    def bill_item(self, s_no,bill_item):
        self.set_font('Arial', '', 12)
        self.set_xy(15,130+(8*s_no))
        self.set_font('Arial', '', 12)
        self.cell(10,10,str(s_no), 0, 0,'C')
        self.set_font('Arial', '', 12)
        if bill_item['po_number']:
            self.set_font('Arial', '', 12)
            self.set_xy(25,130+(8*s_no))
            self.cell(30,10,bill_item['item'].title(), 0, 0,'L')
            self.set_font('Arial', '', 10)
            self.set_xy(55,130+(8*s_no))
            self.cell(30,10,bill_item['po_number'],0,0,'R')
        else:
            self.set_xy(25,130+(8*s_no))
            self.cell(60,10,bill_item['item'].title(), 0, 0,'C')
        self.set_xy(85,130+(8*s_no))
        self.cell(20,10,genes[bill_item['item']], 0, 0,'C')
        self.set_xy(105,130+(8*s_no))
        self.cell(20,10,str(bill_item['uom']), 0, 0,'C')
        self.set_xy(125,130+(8*s_no))
        self.cell(20,10,str(bill_item['qty']), 0, 0,'C')
        self.set_xy(145,130+(8*s_no))
        self.cell(25,10,str(bill_item['rate']), 0, 0,'C')
        self.set_xy(170,130+(8*s_no))
        self.cell(25,10,str(round(bill_item['qty']*bill_item['rate'],2)), 0, 0,'C')

    def bill_items(self, bill_items):
        s_no=1
        total_amt = 0
        for bill_item in bill_items:
            self.bill_item(s_no,bill_item)
            s_no +=1
            total_amt += round(bill_item['qty']*bill_item['rate'],2)
        self.all_details['total_amt'] = total_amt
        self.set_font('Arial', 'B', 12)
        self.set_xy(145, 195)
        self.cell(25,8,"Total", 0, 1,'C')
        self.set_font('Arial', '', 12)
        self.set_xy(170, 195)
        self.cell(25,8,str(round(total_amt,2)), 0, 1,'R')
        
    def expense(self, bags, weight,expenses):
        amount = self.all_details['total_amt']
        exp = {}
        exp['tulai'] = round(expenses['tulai']*amount/100,2) if expenses else 0
        exp['dharmada'] = round(expenses['dharmada']*amount/100,2) if expenses else 0
        exp['wages'] = round(expenses['wages']*weight,2) if expenses else 0
        exp['sutli'] = round(expenses['sutli']*bags,2) if expenses else 0
        exp['commision'] = round(expenses['commision']*amount/100,2) if expenses else 0
        exp['loading_charges'] = round(expenses['loading_charges']*bags,2) if expenses else 0
        exp['vikas_shulk'] = round(expenses['vikas_shulk']*amount/100,2) if expenses else 0
        exp['mandi_shulk'] = round(expenses['mandi_shulk']*amount/100,2) if expenses else 0
        exp['bardana'] = round(expenses['bardana']*bags,2) if expenses else 0
        exp['others'] = round(expenses['others'],2) if expenses else 0
        exp['total'] = round(sum(exp.values()),2)
        self.all_details['expenses'] = exp['total']
        self.set_font('Arial', 'B', 10)
        self.set_xy(25, 195)
        self.cell(30,6,"Loading Charges", 0, 1,'C')
        self.set_font('Arial', '', 10)
        self.set_xy(25, 201)
        self.cell(30,6,str(exp['loading_charges']), 0, 1,'C')
        self.set_font('Arial', 'B', 10)
        self.set_xy(55, 195)
        self.cell(30,6,"Dharmada", 0, 1,'C')
        self.set_font('Arial', '', 10)
        self.set_xy(55, 201)
        self.cell(30,6,str(exp['dharmada']), 0, 1,'C')
        self.set_font('Arial', 'B', 10)
        self.set_xy(25, 207)
        self.cell(30,6,"Mandi Shulk", 0, 1,'C')
        self.set_font('Arial', '', 10)
        self.set_xy(25, 213)
        self.cell(30,6,str(exp['mandi_shulk']), 0, 1,'C')
        self.set_font('Arial', 'B', 10)
        self.set_xy(55, 207)
        self.cell(30,6,"Vikas Shulk", 0, 1,'C')
        self.set_font('Arial', '', 10)
        self.set_xy(55, 213)
        self.cell(30,6,str(exp['vikas_shulk']), 0, 1,'C')
        self.set_font('Arial', 'B', 10)
        self.set_xy(85, 195)
        self.cell(20,6,"Tulai", 0, 1,'C')
        self.set_font('Arial', '', 10)
        self.set_xy(85, 201)
        self.cell(20,6,str(exp['tulai']), 0, 1,'C')
        self.set_font('Arial', 'B', 10)
        self.set_xy(85, 207)
        self.cell(20,6,"Sutli", 0, 1,'C')
        self.set_font('Arial', '', 10)  
        self.set_xy(85, 213)
        self.cell(20,6,str(exp['sutli']), 0, 1,'C')
        self.set_font('Arial', 'B', 10)
        self.set_xy(105, 195)
        self.cell(20,6,"Wages", 0, 1,'C')
        self.set_font('Arial', '', 10)
        self.set_xy(105, 201)
        self.cell(20,6,str(exp['wages']), 0, 1,'C')
        self.set_font('Arial', 'B', 10)
        self.set_xy(105, 207)
        self.cell(20,6,"Bardana", 0, 1,'C')
        self.set_font('Arial', '', 10)  
        self.set_xy(105, 213)
        self.cell(20,6,str(exp['bardana']), 0, 1,'C')
        self.set_font('Arial', 'B', 10)
        self.set_xy(125, 195)
        self.cell(20,6,"Commision", 0, 1,'C')
        self.set_font('Arial', '', 10)
        self.set_xy(125, 201)
        self.cell(20,6,str(exp['commision']), 0, 1,'C')
        self.set_font('Arial', 'B', 10)
        self.set_xy(125, 207)
        self.cell(20,6,"Other", 0, 1,'C')
        self.set_font('Arial', '', 10)  
        self.set_xy(125, 213)
        self.cell(20,6,str(exp['others']), 0, 1,'C')
        self.set_font('Arial', 'B', 12)
        self.set_xy(145, 203)
        self.cell(25,8,"Expenses", 0, 1,'C')
        self.set_font('Arial', '', 12)  
        self.set_xy(170, 203)
        self.cell(25,8,str(round(exp['total'],2)), 0, 1,'R')

    def amount_to_words(self, amount):
        word = number_to_word(amount)
        self.set_font('Arial', 'B', 10)
        self.set_xy(15, 219)
        self.cell(130,8,"Amount in Word", 0, 1,'L')
        self.set_font('Arial', '', 10)
        self.set_xy(15, 227)
        self.cell(130,8,word, 0, 1,'L')

    def terms_conditions(self):
        self.set_font('Arial', '', 12)
        self.set_xy(15, 235)
        self.cell(20,5,"Note :", 0, 1,'L')
        self.set_font('Arial', '', 10)
        self.set_xy(15,240)
        self.cell(20,6,"(1) All Disputes are subject of Anoopshahr Jurisdiction.", 0, 1,'L')
        self.set_xy(15,246)
        self.cell(20,6,"(2) Interest 18% will be charged if not paid within 5 days. E. & O.E.", 0, 1,'L')
        
    def bank_details(self, bank_details):
        self.set_xy(15,252)
        self.set_font('Arial', '', 10)
        self.cell(65,5,"Bank Details", 0,0,'C')
        self.set_xy(15,257)
        self.set_font('Arial', '', 10)
        self.cell(20,5,"Bank Name : "+bank_details['bank_name'].title(), 0,0,'L')
        self.set_xy(15,262)
        self.set_font('Arial', '', 10)
        self.cell(20,5,"Bank A/C No : "+bank_details['bank_account_no'], 0,0,'L')
        self.set_xy(15,267)
        self.set_font('Arial', '', 10)
        self.cell(20,5,"Bank IFSC Code : "+bank_details['bank_ifsc'], 0,0,'L')
        self.set_xy(15,272)
        self.set_font('Arial', '', 10)
        self.cell(20,4,"Bank Branch : "+bank_details['bank_branch'], 0,0,'L')
    
    def pre_authenticated(self, company_name):
        self.set_xy(80,252)
        self.cell(55,5,"Pre Authenticated", 0,0,'C')
        self.set_xy(80,257)
        self.set_font('Times', 'B', 12)
        self.cell(55,10,company_name, 0,0,'C')
        self.set_xy(80,274)
        self.set_font('Arial', '', 10)
        self.cell(55,2,"Prop./Auth. Signatory", 0,0,'C')
    
    def signatory(self, company_name):
        self.set_xy(135,252)
        self.cell(60,5,"Certified and Verified", 0,0,'C')
        self.set_xy(135,257)
        self.set_font('Times', 'B', 14)
        self.cell(60,10,company_name, 0,0,'C')
        self.set_xy(135,274)
        self.set_font('Arial', '', 10)
        self.cell(55,2,"Authorised Signatory", 0,0,'C')
    
    def final_fun(self, frieght):
        total = self.all_details['total_amt'] + self.all_details['expenses']
        round_off = round(round_school(total)-round(total,2),2)
        self.set_xy(145, 211)
        self.set_font('Arial', 'B', 12)
        self.cell(25,8,"Round off", 0,0,'C')
        self.set_xy(170, 211)
        self.set_font('Arial', '', 12)
        self.cell(25,8,str(round_off), 0,0,'R')
        self.all_details['round_off'] = round_off
        total = round_school(sum(self.all_details.values()))
        self.set_xy(145, 219)
        self.set_font('Arial', 'B', 12)
        self.cell(25,8,"Total", 0,0,'C')
        self.set_xy(170, 219)
        self.set_font('Arial', '', 12)
        self.cell(25,8,str(total), 0,0,'R')
        self.set_xy(145, 227)
        self.set_font('Arial', 'B', 12)
        self.cell(25,8,"Frieght", 0,0,'C')
        self.set_xy(170, 227)
        self.set_font('Arial', '', 12)
        self.cell(25,8,str(frieght), 0,0,'R')
        total = round_school(sum(self.all_details.values())+frieght)
        self.set_xy(135, 235)
        self.set_font('Arial', 'B', 12)
        self.cell(35,17,"Grand Total", 0,0,'C')
        self.set_xy(170, 235)
        self.set_font('Arial', '', 12)
        self.cell(25,17,str(total), 0,0,'R')
        self.amount_to_words(total)
    
    def total_s(self,qty,uom):
        self.set_xy(85, 185)
        self.set_font('Arial', 'B', 12)
        self.cell(20,10,"Total", 0,0,'C')
        self.set_xy(125, 185)
        self.set_font('Arial', 'B', 12)
        self.cell(20,10,str(round(qty,2)), 0,0,'C')
        self.set_xy(105, 185)
        self.set_font('Arial', 'B', 12)
        self.cell(20,10,str(round(uom,2)), 0,0,'C')
    
    def remarks(self,remarks):
        if remarks:
            self.set_font('Arial', '', 12)
            self.set_xy(25, 185)
            self.cell(60,10,remarks, 0, 1,'L')
