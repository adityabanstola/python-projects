import qrcode 
import image


qr = qrcode.QRCode(
    version = 15 , #15 means version of qr code ,the high the number bigger the code image and complicateed picture
    box_size = 10 , #size of the box where qr code will be displayed 
    border= 5 # it is the white part of the image -- border in all 4 sides with white color
)
data = "https://www.youtube.com/watch?v=pTkuGR30NhE&ab_channel=AdityaBanstola"
#  i have given the path of the my channel like the same way you can give 
#if you dont want to redirect and create for normal text that write text in the quotes 

qr.add_data(data)
qr.make(fit = True)
img = qr.make_image(fill="black",back_color="white")
img.save("test.png")