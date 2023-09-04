from django.shortcuts import render
from rest_framework import  viewsets,status
from rest_framework.response import  Response
from .serializers import SelfMailSerializer
from .models import SelfMailModel, HeaderAndFooter, Newsletter
from rest_framework.decorators import api_view
from django.core.mail import send_mail,EmailMessage, BadHeaderError
from django.core.exceptions import ObjectDoesNotExist
import openai
import socket
from urllib.error import URLError
from decouple import config
from smtplib import SMTPConnectError, SMTPSenderRefused
import cloudinary.uploader
# Initialize the OpenAI API with your API key
openai.api_key = config('OPENAI_API_KEY')

# Create your views here.

class SelfMailViews(viewsets.ModelViewSet):
    """ This handles CRUD functionality"""
    serializer_class = SelfMailSerializer
    queryset = SelfMailModel.objects.all()


@api_view(['GET', 'POST'])
def openai_function(request):
    #Accept the description from the frontend
    if request.method == 'POST':
        description = request.data.get('description')
        try:
            #Send it to OpenAi
            response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": description}
                        ]
                    )
            #Get OpenAi response and push to the frontend
            generated_text = response['choices'][0]['message']['content']

            return Response({'generated_text': generated_text})
        except ObjectDoesNotExist:
            return Response({'message': 'Description not found'})
        except socket.gaierror as dns_error:
            return Response({'message': 'No network connection'})
        except URLError as e_error:
            return Response({'message': 'Poor or No network connection'})
        except Exception as e:
            return Response({'message': "An error occured"})
    else: 
        return Response({'message': 'No AI Completion'})

@api_view(['GET', 'POST'])
def send_email(request):
    #Accept the details from the frontend
    if request.method == "POST":
        from_email = request.data.get('from_mail')
        to_email = request.data.get('to_mail')
        subject = request.data.get('subject')
        files = request.FILES.getlist('file')
        description = request.data.get('description')

        try:
            #Check for the images in the model 
            header_footer = HeaderAndFooter.objects.latest('date_created')
            if header_footer:
                header_image = header_footer.header_image
                footer_image = header_footer.footer_image
            #Check for the image url
            if header_image:
                existing_header_image = HeaderAndFooter.objects.get(header_image=header_image).header_image_url
                if existing_header_image:
                    header_image_url = existing_header_image
                else :
                    cloudinary_header_image = cloudinary.uploader.upload(header_image, folder="Sme_header_photos")
                    header_image_url = cloudinary_header_image['secure_url']
                    header_footer.header_image_url =  header_image_url
                    header_footer.save()
            if footer_image:
                existing_footer_image = HeaderAndFooter.objects.get(footer_image=footer_image).footer_image_url
                if existing_footer_image:
                    footer_image_url = existing_footer_image
                else:
                    cloudinary_footer_image = cloudinary.uploader.upload(footer_image, folder="Sme_footer_photos")
                    footer_image_url = cloudinary_footer_image['secure_url']
                    header_footer.footer_image_url = footer_image_url
                    header_footer.save()
            
            #Put it into a html fie to send to a user
            email_content = f"""
                    <html>
                    <body>
                        <img src="{header_image_url}" alt="Header Image" style="width: 100%"; height:15vh" />
                        <pre>{description}</pre>
                        <img src="{footer_image_url}" alt="Footer Image" style="width: 100%"; height:15vh" />
                    </body>
                    </html>
                """
            #Construct theemail and send
            email = EmailMessage(subject, email_content, from_email, [to_email])
            email.content_subtype = "html"  # Set the content type to HTML


            if files:
                email.attach(files.name, files.read(), files.content_type)
            email.send()

            #Save the email to your model
            email_record = SelfMailModel(
                from_mail=from_email,
                to_mail=to_email,
                subject=subject,
                file=files,
                description=description,
            )
            email_record.save()

            #Push the email details to the frontend
            email_details= {
                'from_mail': from_email,
                'to_mail': to_email,
                'subject': subject,
                'description': description,
                'date_created': email_record.date_created,
                'file': str(files) if files else None

            }
            return Response({'message': 'Email sent successfully', 'email_details': email_details})
        except BadHeaderError:
            return Response({'message': 'Invalid header found in email'})
        except socket.gaierror as dns_error:
            return Response({'message': 'No DNS network connection'})
        except URLError as e_error:
            return Response({'message': 'Poor or No network connection'})
        except ObjectDoesNotExist:
            return Response({'message': 'Email not found'})
        except SMTPConnectError as smtp_connect_error:
            return Response({'message': 'Error connecting to the SMTP server'})
        except SMTPSenderRefused as sender_refused_error:
            return Response({'message': 'Sender not registered with the SMTP server'})
        except Exception as e:
            return Response({'message': "An error occured"})
    else:
        return Response({'message': 'No Emails Sent yet'})

@api_view(['GET', 'POST'])
def newsletter(request):
    if request.method == 'POST':
        newsletter = request.data.get('newsletter')

        new_newsletter_email = Newsletter(newsletter=newsletter)
        new_newsletter_email.save()
        return Response({'message': 'Email saved successfully'})
    else:
        return Response({'message':'No newsletter '})

