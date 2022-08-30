PyWIG
=====

The main entry point for starting the integration is the ``PyWig`` class.
The following example show you how to initialise the class to start exploring the WatchItGrow data.

.. code-block:: python

   wig = Wig()
   wig.authenticate_basic('your_wig_username', 'your_wig_password)

Next up you can use of the functions below to start interacting with your fields and data in WatchItGrow.

.. autoclass:: pywig.Wig
    :members:
