QrCodeGenerator
===============

To run this application, install the required dependencies:

.. code-block:: shell

    python -m venv venv
    source venv/bin/activate
    pip install -U pip
    pip install -r requirements.txt

To run a local web GUI, execute

.. code-block:: shell

    python app.py

Alternatively, you may run a simple GUI application via

.. code-block:: shell

    python code_generator_ui.py

If you prefer creating your QR codes from the command-line, look at the
tool's help

.. code-block:: shell

    python code_generator.py --help

Using this method, you can generate multiple QR codes at once by passing
the name of a simple CSV file containing the URLs and the output filenames.
For example

.. code-block:: csv

    URL,Filename
    http://example.com,example.com.png
    http://github.com,gh.png
