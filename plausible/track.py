import streamlit.components.v1 as components


def track(message: str):
    html = f"""
<html>
  <head>
    <!-- Plausible tracking code -->
  <script defer data-domain="streamlit.vizzuhq.com"
    src="https://plausible.io/js/script.tagged-events.js"></script>

  <script>
      // JavaScript code to track the custom event when the page loads
      document.addEventListener('DOMContentLoaded', function() {{
        plausible('{message}'); // Track the custom event when the page loads
      }});
    </script>
  </head>
  <body></body>
</html>
    """

    components.html(html, height=0, width=0)
