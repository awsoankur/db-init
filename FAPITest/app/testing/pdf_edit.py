from PyPDF2 import PdfWriter, PdfReader, Transformation
import io
from reportlab.pdfgen.canvas import Canvas
from datetime import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))

# class GenerateFromTemplate:
#     def __init__(self,template):
#         self.template_pdf = PdfReader(open(template, "rb"))
#         self.template_page= self.template_pdf.pages[-2]

#         self.packet = io.BytesIO()
#         self.c = Canvas(self.packet,pagesize=(self.template_page.mediabox.width,self.template_page.mediabox.height))

    
#     def addText(self,text,point):
#         self.c.drawString(point[0],point[1],text)

#     def merge(self):
#         self.c.save()
#         self.packet.seek(0)
#         result_pdf = PdfReader(self.packet)
#         result = result_pdf.pages[0]

#         self.output = PdfWriter()

#         op = Transformation().rotate(0).translate(tx=0, ty=0)
#         result.add_transformation(op)
#         self.template_page.merge_page(result)
#         self.output.add_page(self.template_page)
    
#     def generate(self,dest):
#         outputStream = open(dest,"wb")
#         self.output.write(outputStream)
#         outputStream.close()

locations={
    16 : {
        "date_of_arrangement" : "215,701",
        "place_of_arrangement" : "215,690",
        "name":"215,679",
        "aadhaar":"215,668",
        "pan_number":"215,657",
        "dob":"215,646",
        "phone":"215,635",
        "email":"215,613",
        "res_address1":"215,602",
        "res_address2":"215,591",
        "res_address3":"215,580",
        "office_address1":"215,570",
        "office_address2":"215,560",
        "office_address3":"215,550",
        "nature_of_activities1":"215,539",
        "nature_of_activities2":"215,528",
        "particulars_for_notice":"215,517",
        "account_number":"310,507",
        "account_name":"300,486",
        "bank_name":"290,466",
        "branch":"294,446",
        "ifsc":"283,425"
    },
    17 :{
        "name": "90,682",
        "residingAddress": "125,665",
        "permAddress1":"230,650",
        "permAddress1":"82,634",
        "permAddress1":"82,619",
    }
}

template_pdf = PdfReader(open("test.pdf","rb"))
pages = template_pdf.pages
# pages_to_edit=[[i,pages[i]] for i in range(len(pages))]
pages_to_edit=[[16,pages[16]],[17,pages[17]]]
output = PdfWriter()
# for page in pages[:-3]:
#     output.add_page(page)
for i in range(len(pages_to_edit)):
    page = pages_to_edit[i][1]
    mirror_page = pages_to_edit[i][0]
    packet = io.BytesIO()
    c =Canvas(packet, pagesize= (page.mediabox.width,page.mediabox.height))
    c.setFontSize(size= 8) 
    c.setFont("VeraIt",8)  
    # c.setFont("Courier",8) 

    c.drawString(460,40,"Digitally Signed by")
    c.drawString(460,30,"Name: ")
    c.drawString(460,20,"Time :" + datetime.today().strftime("%d %B %Y, %H:%M:%S"))
    # if mirror_page == 16:
    #     c.drawString(215,701,"test test test test test")
    #     c.drawString(215,690,"test test test test test")
    #     c.drawString(215,679,"test test test test test")
    #     c.drawString(215,668,"test test test test test")
    #     c.drawString(215,657,"test test test test test")
    #     c.drawString(215,646,"test test test test test")
    #     c.drawString(215,635,"test test test test test")
    #     c.drawString(215,624,"test test test test test")
    #     c.drawString(215,517,"test test test test test")
    #     c.drawString(310,507,"test test test test test")
    #     c.drawString(300,486,"test test test test test")
    #     c.drawString(290,466,"test test test test test")
    #     c.drawString(294,446,"test test test test test")
    #     c.drawString(283,425,"test test test test test")
    # elif mirror_page == 17:
    #     c.drawString(125,665,"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    #     c.drawString(230,650,"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    #     c.drawString(82,634,"test test test test test")
    #     c.drawString(82,619,"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    c.save()
    packet.seek(0)
    result_page = PdfReader(packet).pages[0]
    result_page.merge_page(pages[mirror_page])
    result_page.compress_content_streams()
    output.add_page(result_page)
# output.add_page(pages[-1])

outputStream = open("output.pdf","wb")
output.write(outputStream)
outputStream.close()