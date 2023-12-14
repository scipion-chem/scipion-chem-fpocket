=======================
Fpocket plugin
=======================

**Documentation under development, sorry for the inconvenience**

This is a **Scipion** plugin that offers different tools from the
`FPocket suite <https://github.com/Discngine/fpocket>`_.
These tools will make it possible to carry out different functions for predicting protein pockets.

You can find further information on the
`plugin documentation <https://scipion-chem.github.io/docs/plugins/fpocket/index.html>`_.

==========================
Install this plugin
==========================

You will need to first install
`Scipion3 <https://scipion-em.github.io/docs/release-3.0.0/docs/scipion-modes/how-to-install.html>`_  and
`Scipion-chem <https://github.com/scipion-chem/scipion-chem>`_ to run these protocols.


1. **Install the plugin in Scipion**

Fpocket is installed automatically by scipion.

- **Install the stable version (Not available yet)**

    Through the plugin manager GUI by launching Scipion and following **Configuration** >> **Plugins**

    or

.. code-block::

    scipion3 installp -p scipion-chem-fpocket


- **Developer's version**

    1. **Download repository**:

    .. code-block::

        git clone https://github.com/scipion-chem/scipion-chem-fpocket.git

    2. **Switch to the desired branch** (master or devel):

    Scipion-chem-fpocket is constantly under development and including new features.
    If you want a relatively older an more stable version, use master branch (default).
    If you want the latest changes and developments, user devel branch.

    .. code-block::

                cd scipion-chem-fpocket
                git checkout devel

    3. **Install**:

    .. code-block::

        scipion3 installp -p path_to_scipion-chem-fpocket --devel


