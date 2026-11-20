from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.template.loader import render_to_string


class AdminPermissionsPolicyTests(TestCase):
    def test_admin_allows_unload_events(self):
        response = self.client.get(reverse('admin:index'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('unload', response.headers.get('Permissions-Policy', ''))
        self.assertIn('self', response.headers.get('Permissions-Policy', ''))


class BaseTemplateRenderingTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_base_template_renders_ptvti_brand_elements(self):
        request = self.factory.get('/')
        rendered_html = render_to_string('base.html', request=request)

        # Brand identity checks
        self.assertIn('PALAZZOLO', rendered_html)
        self.assertIn('Technical &amp; Vocational Training Institute', rendered_html)
        self.assertIn('variables.css', rendered_html)
        self.assertIn('navigation.css', rendered_html)
        self.assertIn('footer.css', rendered_html)
        self.assertIn('main.js', rendered_html)
        self.assertIn('TVETA Accredited', rendered_html)

