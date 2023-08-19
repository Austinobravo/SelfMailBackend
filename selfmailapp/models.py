from django.db import models

# Create your models here.
#The Email Model
class SelfMailModel(models.Model):
    from_mail = models.EmailField(help_text='The sender of the mail.')
    to_mail = models.EmailField(help_text='The receiver of the mail')
    subject = models.CharField(max_length=500, help_text='The heading of the mail')
    file = models.FileField(help_text='A pdf you want to send.', null=True, blank=True)
    description = models.TextField(help_text='The description/mail')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email to: {self.to_mail} from {self.from_mail}"

    class Meta:
        verbose_name = 'SelfMail'
        verbose_name_plural = 'SelfMail'

#The Email Images And Urls
class HeaderAndFooter(models.Model):
    header_image = models.ImageField(null=True, blank=True, help_text='The header',default="header_image.jpeg")
    footer_image = models.ImageField(null=True, blank=True,help_text='The footer', default="footer_image.jpeg")
    header_image_url = models.URLField(null=True, blank=True, help_text="The header url - Don't Edit.")
    footer_image_url = models.URLField(null=True, blank=True, help_text="The Footer url - Don't Edit.")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str("Header")

    class Meta:
        verbose_name = 'header_and_footer'
        verbose_name_plural = 'header_and_footer'

#Newsletter
class Newsletter(models.Model):
    newsletter = models.CharField(max_length=100, help_text="The newsletter email")

    def __str__(self):
        return self.newsletter
    
    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletter'
