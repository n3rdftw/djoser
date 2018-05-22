from django.contrib.auth.tokens import default_token_generator

from templated_mail.mail import BaseEmailMessage

from djoser import utils
from djoser.conf import settings
from rest_framework_jwt.settings import api_settings


class ActivationEmail(BaseEmailMessage):
    template_name = 'email/activation.html'

    def get_context_data(self):
        context = super(ActivationEmail, self).get_context_data()

        user = context.get('user')
        context['uid'] = utils.encode_uid(user.pk)
        context['token'] = default_token_generator.make_token(user)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        # TODO - migrate off needing this in activation email
        context['jwt_token'] = jwt_encode_handler(payload)
        context['url'] = settings.ACTIVATION_URL.format(**context)
        return context


class ConfirmationEmail(BaseEmailMessage):
    template_name = 'email/confirmation.html'


class PasswordResetEmail(BaseEmailMessage):
    template_name = 'email/password_reset.html'

    def get_context_data(self):
        context = super(PasswordResetEmail, self).get_context_data()

        user = context.get('user')
        context['uid'] = utils.encode_uid(user.pk)
        context['token'] = default_token_generator.make_token(user)
        context['url'] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        return context
