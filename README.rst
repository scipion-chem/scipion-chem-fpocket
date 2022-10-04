=======================
Fpocket plugin
=======================

**Documentation under development, sorry for the inconvenience**

This is a **Scipion** plugin that offers different **fpocket tools**.
These tools will make it possible to carry out different functions for predicting protein pockets

Therefore, this plugin allows to use programs from the fpocket software suite
within the Scipion framework.

==========================
Install this plugin
==========================

You will need to use `Scipion3 <https://scipion-em.github.io/docs/docs/scipion
-modes/how-to-install.html>`_ to run these protocols.


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


