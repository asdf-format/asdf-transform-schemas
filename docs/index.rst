.. _asdf-transform-schemas:

**********************
ASDF Transform Schemas
**********************

The ASDF Transform Schemas define a set of schemas for serializing the models defined by
:ref:`astropy.modeling <astropy:astropy-modeling>` for the ASDF file format. These schemas
are based upon the schemas in the :ref:`ASDF Standard <asdf-standard:asdf-standard>` and
are packaged for use by the :ref:`ASDF <asdf:asdf>` library.

.. note::
   This is only a schema package, to use these schemas to serialize astropy models,
   one must install the :ref:`asdf-astropy <asdf-astropy:asdf-astropy>` package.

Included Resources
==================

The following are listings of all the schemas provided by this package for ASDF.

.. note::
  Typically, schemas are used in ASDF via their tag, which can be found in the manifest.
  Using a transform in ASDF it is recommended that you use the tag instead of a direct
  reference to the schema. When doing so make sure you are using the correct manifest version.

.. toctree::
  :maxdepth: 1

  transforms.rst
  legacy.rst
  manifests.rst

Developer Resources
===================

.. toctree::
  :maxdepth: 1

  contributing.rst
  changes.rst

Index
=====

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
