#from django.test import TestCase

# Create your tests here.
#pip install pdf2image
#Once installed you can use following code to get images.

from pdf2image import convert_from_path
pages = convert_from_path('2.pdf', 50)

#Saving pages in jpeg format

for page in pages:
    page.save('out2.jpg', 'JPEG')